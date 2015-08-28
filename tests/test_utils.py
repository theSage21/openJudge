import pytest
from openjudge import errors
from openjudge.utils import (get_random_string,
                             run_command,
                             get_result,
                             get_file_from_url,
                             check_execution,
                             get_json,)


def test_get_random_string():
    a = get_random_string()
    b = get_random_string()
    assert a != b


def test_get_random_string_of_specified_length():
    a = get_random_string(20)
    b = get_random_string(100)
    assert len(a) == 20
    assert len(b) == 100


def test_run_command_return_type():
    cmd = 'echo hi'
    r_val, out, err = run_command(cmd)
    assert r_val == 0
    assert out == 'hi\n'
    assert err == ''


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
    assert out == ''


def test_get_result_catchall():
    re = get_result(tuple(), 'a', 'b')
    assert re == 'Contact a volunteer'
    assert isinstance(re, str)


def test_get_result_correct_zero_return(tmpdir):
    p = tmpdir.join('expected')
    p.write('1\n4')
    got = '1\n4'
    re = get_result(0, str(p), got)
    assert re == 'Correct'


def test_get_result_incorrect_zero_return(tmpdir):
    p = tmpdir.join('expected')
    p.write('1\n4')
    got = '1\n2'
    re = get_result(0, str(p), got)
    assert re == 'Incorrect'


def test_get_result_error_non_zero_return():
    expected = 'this_does_not_matter'
    re = get_result(1, expected, 'so_does_this')
    assert re == 'Error'


def test_get_result_timeout_None_return():
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


def test_get_json_raises_interface_not_running():
    with pytest.raises(errors.InterfaceNotRunning):
        get_json('http://e.com/some/url/')


def test_get_file_from_url_unable_to_retrieve_url():
    url = 'http://example.com/some/exist.html'
    with pytest.raises(errors.InterfaceNotRunning):
        get_file_from_url(url, 'filename')


def test_get_file_from_url_folder_does_not_exist_no_overwrite(httpserver, tmpdir):
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


def test_get_file_from_url_overwrite_file_exists(httpserver, tmpdir):
    httpserver.serve_content('nothing')
    url = httpserver.url
    name = url.split('/')[-1]
    # create the file
    p = tmpdir.join(name)
    p.write('something')
    assert p.read() == 'something'
    # get the file
    path = get_file_from_url(url, str(tmpdir), True)
    # check
    assert p.read() == 'nothing'
    assert str(p) == path
