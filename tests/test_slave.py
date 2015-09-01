import os
import pytest
import socket
import logging
from socket import create_connection
from openjudge import config
from openjudge.slave import Slave
from json import loads, dumps


@pytest.fixture
def slave(httpserver):
    # data provided by the setup script
    content = '''{"question": {"1": {"type": 2, "out":
                  "/media/test_cases/out", "inp":
                  "/media/test_cases/inp"}}, "language":
                  {"2": {"overwrite": false, "misc":
                  "g++.sh", "wrap": "/media/wrappers/g.sh"}
                  , "5": {"overwrite": false, "misc":
                  "python3.sh", "wrap":
                  "/media/wrappers/python3.sh"},
                  "3": {"overwrite": false, "misc":
                  "python2.sh", "wrap":
                  "/media/wrappers/python2.sh"}, "4":
                  {"overwrite": false, "misc": "gcc.sh",
                  "wrap": "/media/wrappers/gcc.sh"}, "1":
                  {"overwrite": false, "misc": "java.sh",
                  "wrap": "/media/wrappers/java.sh"}}}'''
    httpserver.serve_content(content)
    url = httpserver.url[7:]  # cut out the already existing http://
    config.timeout_limit = 10
    config.check_data_folder = '/tmp/check_data'
    config.webserver = '127.0.0.1:8000'
    config.detail_url = '/question/detail_list/'
    config.listen_addr = ('127.0.0.1', 9000)
    config.job_list_prefix = 'joblist_'
    config.protocol_of_webserver = 'http://'
    config.logfile = 'judge.log'
    config.default_loglevel = 30

    class SlaveFactory:
        def get(self):
            s = Slave(webserver=url,
                      detail_url='/',
                      listen_addr=('127.0.0.1', 9000),
                      # listen_addr=('127.0.0.1', random.choice(range(9000, 10000))),
                      timeout_limit=20,
                      loglevel=logging.DEBUG)
            assert s.check_data['question'] != {}
            assert s.check_data['language'] != {}
            return s
    return SlaveFactory()


def test_slave_creation_failure():
    s = Slave(webserver='127.0.0.1:8000',
              detail_url='/somethnig/')
    assert not hasattr(s, 'check_data')


def test_slave_creation_with_all_parameters(httpserver):
    httpserver.serve_content('{"question": {}, "language": {}}')
    url = httpserver.url[7:]  # cut out the already existing http://
    assert Slave(webserver=url,
                 detail_url='/',
                 listen_addr=('127.0.0.1', 9000),
                 timeout_limit=20)


def test_slave_creation_with_no_parameters(httpserver, slave):
    slave = slave.get()
    assert slave


def test_slave_job_list_read_existing_file(httpserver):
    # custom joblist file name
    with open('joblist_9000', 'w') as p:
        p.write('{"1": "2"}')
    # create a slave
    httpserver.serve_content('{"question": {}, "language": {}}')
    url = httpserver.url[7:]  # cut out the already existing http://
    s = Slave(webserver=url,
              detail_url='/',
              listen_addr=('127.0.0.1', 9000),
              timeout_limit=20)
    assert s.name == 'joblist_9000'
    assert s
    assert s.job_list == {"1": "2"}
    os.remove('joblist_9000')


def test_slave_job_list_without_existing_file(slave):
    # custom joblist file name
    # create a slave
    s = slave.get()
    assert s
    assert s.job_list == {}


def test_slave_method_get_data_from_socket(slave):
    slave = slave.get()
    slave_addr = slave.sock.getsockname()
    data = {'pk': 1,
            'qno': 1,
            'source': '/',  # the process only needs to get the data
            'name': 'some.py',
            'language': '1',
            }
    data_string = dumps(data)
    sock = create_connection(slave_addr)
    sock.sendall(data_string.encode('utf-8'))
    data_recv, com = slave.get_data_from_socket()
    com.close()
    assert data_recv == data


def test_slave_assign_to_job_list(slave):
    data = {'pk': 1, 'qno': 1,
            'source': '/media/test_cases/inp',  # it does not matter
            'name': 'some.py',
            'language': '1', }
    slave = slave.get()
    result = loads(slave.assign_to_job_list(data))
    assert result[0] == 'Error'


def test_slave_assign_to_job_two_times(slave):
    data = {'pk': 1, 'qno': '1',
            'source': '/media/test_cases/inp',  # it does not matter
            'name': 'some.py',
            'language': '1', }
    slave = slave.get()
    result = loads(slave.assign_to_job_list(data))
    assert result[0] == 'Error'
    result = loads(slave.assign_to_job_list(data))
    assert result[0] == 'Error'


def test_slave_shutdown_procedure(slave):
    assert slave.get().shutdown() is None


def test_slave_request_validation(slave):
    data = {'pk': 1, 'qno': '1',
            'source': '/media/test_cases/inp',  # it does not matter
            'name': 'some.py',
            'language': '1', }
    valid = slave.get().is_valid_request(data)
    assert valid


def test_slave_request_invalidity(slave):
    data = {'pk': 1, 'qno': 'not_a_valid_pk',
            'source': '/media/test_cases/inp',  # it does not matter
            'name': 'some.py',
            'language': '1', }
    slave = slave.get()
    valid = slave.is_valid_request(data)
    assert not valid
    data['language'] = 'again not valid'
    data['qno'] = '1'  # totally valid
    valid = slave.is_valid_request(data)
    assert not valid


def test_process_request_invalid_request(slave):
    data = {'pk': 1, 'qno': 'not_a_valid_pk',
            'source': '/media/test_cases/inp',  # it does not matter
            'name': 'some.py',
            'language': '1', }
    slave = slave.get()
    result, remark = slave.process_request(data)
    assert result == 'Invalid request'


def test_socket_creation():
    s = Slave()
    assert s.sock


def test_socket_creation_on_already_bound_socket(slave):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 9000))
    a = slave.get()
    assert a.sock.getsockname() != s.getsockname()
    s.close()
