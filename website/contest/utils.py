import os
import subprocess as sp
from queue import Queue
from threading import Thread
from contextlib import contextmanager

Q = Queue()


@contextmanager
def Source(text, path):
    "Remove all source files"
    directory, _ = os.path.split(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(path, 'w') as fl:
        fl.write(text)
    yield path
    os.remove(path)



def is_correct(att, joblist={}):
    if att.pk not in joblist.keys():
        joblist[att.pk] = (None, 'Received')
        t = Thread(target=execute, args=(att,))
        t.start()
    result, remark = recheck_Q(att)
    joblist[att.pk] = result, remark
    print(joblist)
    return joblist[att.pk]


def recheck_Q(att):
    global Q
    result_, remark_ = None, 'Checking'
    temp = Queue()
    while Q.qsize() > 0:
        pk, result, remark = Q.get()
        if pk == att.pk:
            result_, remark_ = result, remark
        else:
            temp.put((pk, result, remark))
    while temp.qsize() > 0:
        Q.put(temp.get())
    return result_, remark_


def execute(att):
    tests = att.question.question_testcase.all()
    wrapper = att.language.wrapper.path
    pre = 'chmod u+x {} &&'.format(wrapper)
    timeout = att.language.timeout * att.question.contest.timeout

    outputs, results, remarks = [], [], []
    path = os.path.join(str(att.pk), att.filename)
    with Source(att.source, path) as source:
        for tst in tests:
            cmd = ' '.join((pre, wrapper, tst.inp.path, source))
            result, output, remark = run(cmd, timeout)
            with open(tst.out.path, 'r') as out:
                expected = out.read()
            outputs.append((output.strip() ==  expected.strip()))
            results.append(result)
            remarks.append(remark)
    result, remarks = process_tests(results, remarks, outputs)
    print(att.pk, result, remarks)
    global Q
    Q.put((att.pk, result, remarks))


def run(cmd, timeout):
    try:
        p = sp.run(cmd,
                   timeout=timeout,
                   stderr=sp.PIPE,
                   stdout=sp.PIPE,
                   shell=True)
    except sp.TimeoutExpired:
        result = None
        stdout, stderr = b'', b''
    else:
        result = (p.returncode == 0)
        stdout, stderr = p.stdout, p.stderr
    return result, stdout.decode(), stderr.decode()


def process_tests(results, remarks, outputs):
    if all(results):
        if all(outputs):
            result = True, 'Correct'
        else:
            result = False, 'Incorrect'
    else:
        if None in results:
            result = False, 'Timeout'
        elif False in results:
            result = False, 'ErrorInCode'
    return result
