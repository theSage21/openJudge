from subprocess import (run, PIPE, TimeoutExpired)


def __run_command__(command, timeout):
    "Run a given command with a set timeout"
    try:
        p = run(command, timeout=timeout,
                stderr=PIPE, stdout=PIPE,
                shell=True)
    except TimeoutExpired:
        result = None
        stdout, stderr = b'', b''
    else:
        result = p.returncode == 0
        stdout, stderr = p.stdout, p.stderr
    return result, stdout.decode(), stderr.decode()
