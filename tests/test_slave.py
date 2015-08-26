import pytest
import random
from socket import create_connection
from openjudge import config, errors
from openjudge.slave import (get_random_string,
                             run_command,
                             get_result,
                             get_file_from_url,
                             check_execution,
                             get_json,
                             Slave,
                             dumps,
                             loads,
                             bcolors)


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
    config.language_url = '/question/detail_list/',  # the process only needs to get the data
    config.listen_addr = ('127.0.0.1', 9000)
    config.timeout_limit = 10
    s = Slave(webserver=url,
              language_url='/',
              listen_addr=('127.0.0.1', random.choice(range(9000, 10000))),
              timeout_limit=20)
    assert s.check_data['question'] != {}
    assert s.check_data['language'] != {}
    return s


def test_get_random_string():
    a = get_random_string()
    b = get_random_string()
    assert a != b


def test_run_command_return_type():
    cmd = 'echo hi'
    r_val, out, err = run_command(cmd)
    assert r_val == 0
    assert out == 'hi\n'


def test_run_command_timeout():
    cmd = 'echo hi;sleep 2; echo done'
    r_val, out, err = run_command(cmd, 1)
    assert err == ''
    assert r_val is None
    assert out == ''


def test_run_command_error():
    cmd = 'cat non_existant_file'
    r, out, err = run_command(cmd)
    assert r == 1
    assert err == 'cat: non_existant_file: No such file or directory\n'


def test_color_sequences_for_printing():
    assert bcolors
    assert bcolors.HEADER
    assert bcolors.OKBLUE
    assert bcolors.OKGREEN
    assert bcolors.WARNING
    assert bcolors.FAIL
    assert bcolors.ENDC
    assert bcolors.BOLD
    assert bcolors.UNDERLINE


def test_get_result_catchall():
    re = get_result(tuple(), 'a', 'b')
    assert re == 'Contact a volunteer'
    assert isinstance(re, str)


def test_get_result_correct(tmpdir):
    p = tmpdir.join('expected')
    p.write('1\n4')
    got = '1\n4'
    re = get_result(0, str(p), got)
    assert re == 'Correct'


def test_get_result_incorrect(tmpdir):
    p = tmpdir.join('expected')
    p.write('1\n4')
    got = '1\n2'
    re = get_result(0, str(p), got)
    assert re == 'Incorrect'


def test_get_result_error():
    expected = 'this_does_not_matter'
    re = get_result(1, expected, 'so_does_this')
    assert re == 'Error'


def test_get_result_timeout():
    expected = 'this_does_not_matter',
    re = get_result(None, expected, 'so_does_this')
    assert re == 'Timeout'


def test_check_execution_correct_exact(tmpdir):
    p = tmpdir.join('expected')
    p.write('1\n4\n9')
    got = '1\n4\n9'
    result = check_execution(str(p), got)
    assert result


def test_check_execution_incorrect_exact(tmpdir):
    p = tmpdir.join('expected')
    p.write('1\n4\n9')
    got = '1\n4\n8'  # this has 8 instead of 9
    result = check_execution(str(p), got)
    assert not result


def test_check_execution_correct_error_range(tmpdir):
    p = tmpdir.join('expected')
    p.write('1\n4\n9')
    got = '1\n3.9999\n8.9999'
    result = check_execution(str(p), got, 0.1)
    assert result


def test_check_execution_incorrect_error_range(tmpdir):
    p = tmpdir.join('expected')
    p.write('1\n4\n9')
    got = '1\n3.1\n8.1'
    result = check_execution(str(p), got, 0.1)
    assert not result


def test_get_json(httpserver):
    httpserver.serve_content('{"a":1}')
    assert get_json(httpserver.url) == {'a': 1}


def test_get_file_from_url_unable_to_retrieve_url():
    url = 'http://example.com/some/exist.html'
    with pytest.raises(errors.InterfaceNotRunning):
        get_file_from_url(url, 'filename')


def test_get_file_from_url_folder_does_not_exist(httpserver, tmpdir):
    httpserver.serve_content('nothing')
    url = httpserver.url
    folder = str(tmpdir) + '/random/'
    fl = get_file_from_url(url, folder)
    assert fl == str(tmpdir) + '/random/' + url.split('/')[-1]


def test_get_file_from_url_no_overwrite_file_exists(httpserver, tmpdir):
    httpserver.serve_content('nothing')
    url = httpserver.url
    name = url.split('/')[-1]
    # create the file
    p = tmpdir.join(name)
    p.write('something')
    assert p.read() == 'something'
    # get the file
    fl = get_file_from_url(url, str(tmpdir))
    # assert a new file was created
    assert p.read() == 'something'
    with open(fl, 'r') as recieved_data:
        assert recieved_data.read() == 'nothing'


def test_get_file_from_url_no_overwrite_file_does_not_exist(httpserver, tmpdir):
    httpserver.serve_content('nothing')
    url = httpserver.url
    path = get_file_from_url(url, str(tmpdir), False)
    name = url.split('/')[-1]
    assert path == str(tmpdir) + '/' + name


def test_slave_creation_failure():
    assert Slave()


def test_slave_creation_with_all_parameters(httpserver):
    httpserver.serve_content('{"question": {}, "language": {}}')
    url = httpserver.url[7:]  # cut out the already existing http://
    assert Slave(webserver=url,
                 language_url='/',
                 listen_addr=('127.0.0.1', 9000),
                 timeout_limit=20)


def test_slave_creation_with_no_parameters(httpserver):
    httpserver.serve_content('{"question": {}, "language": {}}')
    url = httpserver.url[7:]  # cut out the already existing http://
    config.webserver = url
    config.language_url = '/'
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
              language_url='/',
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
