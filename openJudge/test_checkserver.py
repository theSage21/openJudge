from checkserver import (get_random_string,
                         run_command)


def test_get_random_string():
    a = get_random_string()
    b = get_random_string()
    assert a != b


def test_run_command_return_type():
    cmd = 'echo hi'
    r_val, err = run_command(cmd)
    assert r_val == 0


def test_run_command_timeout():
    cmd = 'echo hi;sleep 2; echo done'
    r_val, err = run_command(cmd, 1)
    assert err == ''
    assert r_val is None


def test_run_command_error():
    cmd = 'cat non_existant_file'
    r, err = run_command(cmd)
    assert r == 1
    assert err == 'cat: non_existant_file: No such file or directory\n'
