import os
from openjudge import config, tools
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


def check_results_by_running_code(code, inp_list, out_list, wrap, queue, attempt_id):
    assert len(inp_list) == len(out_list), 'each inp needs an out'
    n_tests_cleared = 0
    codepath = os.path.join(config.working_root, attempt_id)
    inp_paths, code_paths, errors, commands = [], [], [], []
    results = [None] * len(inp_list)
    for inp, out in zip(inp_list, out_list):
        inpath = os.path.join(config.working_root, tools.random_id())
        inp_paths.append(inpath)
        with open(inpath, 'w') as fl:
            fl.write(inp)
        command = wrap.format(code=codepath, input=inpath)
        commands.append(command)
    queue.put({'tests_cleared': n_tests_cleared, 'errors': errors,
               'attempt_id': attempt_id, 'inp_paths': inp_paths,
               'code_paths': code_paths, 'commands': commands,
               'results': results
               })


def get_attempt_status(attempt_id, queue):
    return True, 'All ok'
