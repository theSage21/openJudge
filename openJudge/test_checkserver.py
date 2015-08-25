import os
from checkserver import (get_random_string,
                         run_command,
                         check_execution,
                         bcolors)


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
