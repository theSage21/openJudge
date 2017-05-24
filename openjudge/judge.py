import os
from openjudge import config, tools
from subprocess import (run, PIPE, TimeoutExpired)
from multiprocessing import Queue
from threading import Thread


def __thread_worker__():
    """
    Keep checking the job queue for a job and check it.
    Place it in contest data when it is done.
    """
    global job_queue
    while True:
        attempt = job_queue.get()
        if attempt['tests_cleared'] is None:
            tools.log('Checking attempt {}'.format(attempt['attempt_id']))
            commands = attempt['commands']
            out_list = attempt['out_list']
            attempt['status'] = []
            for command, out_expected in zip(commands, out_list):
                res, out, err = __run_command__(command, config.timeout)
                status = None
                if res == 0:
                    status = out == out_expected
                else:
                    status = None
                    attempt['err_message'] = err
                    attempt['out_message'] = out
                attempt['status'].append(status)
                tools.log('Attempt {} status {}'.format(attempt['attempt_id'],
                                                        status))
            attempt['tests_cleared'] = sum(1 for i in attempt['status'] if i)
            tools.add_attempt_to_contest(attempt['attempt_id'], attempt)


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


# -------------------------------------------------------------
job_queue = Queue()
# Start threads to check the code
for tid in range(config.n_threads_to_check_threads):
    t = Thread(target=__thread_worker__)
    t.start()
    config.code_checking_threads[tid] = t
# -------------------------------------------------------------


def check_results_by_running_code(code, inp_list, out_list, wrap, attempt_id):
    global job_queue
    assert len(inp_list) == len(out_list), 'each inp needs an out'
    codepath = os.path.join(config.working_root, attempt_id)
    with open(codepath, 'w') as fl:
        fl.write(code)
    inp_paths, commands = [], []
    for inp, out in zip(inp_list, out_list):
        inpath = os.path.join(config.working_root, tools.random_id())
        inp_paths.append(inpath)
        with open(inpath, 'w') as fl:
            fl.write(inp)
        command = wrap.format(code=codepath, input=inpath)
        commands.append(command)
    tools.log('Adding attempt {} to job queue'.format(attempt_id))
    job_queue.put({'tests_cleared': None, 'attempt_id': attempt_id,
                   'inp_paths': inp_paths,
                   'code_path': codepath, 'commands': commands,
                   'out_list': out_list
                   })


def get_attempt_status(attempt_id):
    contest = tools.read_contest_json()
    if attempt_id not in contest['attempts'].keys():
        status, remark = None, 'The attempt has been sent to the judge'
    else:
        attempt = contest['attempts'][attempt_id]
        status = attempt['status']
        if any(i is None for i in status):
            remark = attempt['err_message']
            result = None
        elif all(i for i in status):
            remark = 'Cleared {} tests'.format(attempt['tests_cleared'])
            result = True
        elif any(not i for i in status):
            remark = 'Unable to clear some tests.'
            result = False
    return result, remark
