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
        if not attempt['evaluated']:
            attid = attempt['attempt_id']
            tools.log('Checking attempt {}'.format(attid))
            commands = attempt['commands']
            out_list = attempt['out_list']
            attempt['status'] = []
            for command, out_expected in zip(commands, out_list):
                ran_without_error, out, err = __run_command__(command,
                                                              config.timeout)
                status = False if ran_without_error else None
                tools.log(ran_without_error, out, err, '-'*10)
                if ran_without_error:
                    status = all((i.strip() == j.strip())
                                 for i, j in zip(out, out_expected))
                attempt['status'].append(status)
                tools.log('Attempt {} status {}'.format(attid, status))
            attempt['evaluated'] = True
            tools.add_attempt_to_contest(attempt)
        else:
            tools.log('This attempt was in Job queue but checked')
            tools.log(attempt)
            tools.log('*'*50)


def __run_command__(command, timeout):
    "Run a given command with a set timeout"
    try:
        p = run(command, timeout=timeout,
                stderr=PIPE, stdout=PIPE,
                shell=True)
    except TimeoutExpired:
        result = False
        stdout, stderr = b'', b'Timeout'
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


def submit_attempt(code, inp_list, out_list, wrap, attempt_id, user, qpk):
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
    job_queue.put({'evaluated': False, 'attempt_id': attempt_id,
                   'inp_paths': inp_paths,
                   'code_path': codepath, 'commands': commands,
                   'out_list': out_list, 'user': user,
                   'qpk': qpk
                   })


def get_attempt_status(attempt_id):
    with tools.Contest() as contest:
        if attempt_id not in contest['attempts']:
            result, remark = None, 'The attempt has been sent to the judge'
        else:
            attempt = contest['attempts'][attempt_id]
            status = attempt['status']
            if any(i is None for i in status):
                remark = 'The program raised an error'
                result = False
            elif all(status):
                remark = 'Your Program Cleared {} tests'
                remark = remark.format(sum(1 for i in status if i))
                result = True
            elif not all(status):
                remark = 'Your Program did not clear some tests.'
                result = False
    return result, remark
