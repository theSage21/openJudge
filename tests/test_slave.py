from openjudge.slave import (get_random_string,
                             run_command,
                             get_result,
                             check_execution,
                             bcolors)


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
