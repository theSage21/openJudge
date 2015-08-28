import pytest
import random
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
    config.webserver = '127.0.0.1:8000'
    config.detail_url = '/question/detail_list/',  # the process only needs to get the data
    config.listen_addr = ('127.0.0.1', 9000)
    config.timeout_limit = 10
    s = Slave(webserver=url,
              detail_url='/',
              listen_addr=('127.0.0.1', random.choice(range(9000, 10000))),
              timeout_limit=20,
              loglevel=logging.DEBUG)
    assert s.check_data['question'] != {}
    assert s.check_data['language'] != {}
    return s


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


def test_slave_creation_with_no_parameters(httpserver):
    httpserver.serve_content('{"question": {}, "language": {}}')
    url = httpserver.url[7:]  # cut out the already existing http://
    config.webserver = url
    config.detail_url = '/'
    assert Slave()


def test_slave_job_list_read_existing_file(tmpdir, httpserver):
    # custom joblist file name
    p = tmpdir.join('job')
    config.job_list_prefix = str(p)
    p = tmpdir.join('job9000')
    p.write('{"1": "2"}')
    # create a slave
    httpserver.serve_content('{"question": {}, "language": {}}')
    url = httpserver.url[7:]  # cut out the already existing http://
    s = Slave(webserver=url,
              detail_url='/',
              listen_addr=('127.0.0.1', 9000),
              timeout_limit=20)
    assert s
    assert s.job_list == {"1": "2"}


def test_slave_job_list_without_existing_file(slave):
    # custom joblist file name
    # create a slave
    s = slave
    assert s
    assert s.job_list == {}


def test_slave_method_get_data_from_socket(slave):
    slave_addr = slave.sock.getsockname()
    data = {'pk': 1,
            'qno': 1,
            'source': '/',  # the process only needs to get the data
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
            'language': '1', }
    result = loads(slave.assign_to_job_list(data))
    assert result[0] == 'Error'


def test_slave_assign_to_job_two_times(slave):
    data = {'pk': 1, 'qno': 1,
            'source': '/media/test_cases/inp',  # it does not matter
            'language': '1', }
    result = loads(slave.assign_to_job_list(data))
    assert result[0] == 'Error'
    result = loads(slave.assign_to_job_list(data))
    assert result[0] == 'Error'


def test_slave_shutdown_procedure(slave):
    assert slave.shutdown() is None
