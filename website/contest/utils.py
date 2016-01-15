import os
import signal
import random
import subprocess
from queue import Queue
from threading import Thread
from json import loads, dumps

results = {}
result_Q = Queue()
ERR = 0.001

def is_correct(att):
    "Is this attempt correct?"
    global results, result_Q
    if att.pk in results.keys():  # not first time
        if results[att.pk] is None:  # not yet done
            check_queue(att)
    else:  # first time
        results[att.pk] = None
        t = Thread(target=execute, args=(att,))
        t.start()
        check_queue(att)
    return results[att.pk]


def check_queue(att):
    "Check if this attempt is in the result queue"
    global results, result_Q
    temp = {}
    while result_Q.qsize() > 0:
        key, val, rem = result_Q.get()
        temp[key] = (val, rem)
    result, comment = None, "Checking..."
    for key, value in temp.items():
        if key == att.pk:
            result, comment = value
        else:
            result_Q.put((key, value[0], value[1]))
    results[att.pk] = result
    return result


def save_text_to_file(text, file_path):
    "Save this text to given file name"
    path, name = os.path.split(file_path)
    with open(file_path, 'w') as fl:
        fl.write(text)


def execute(att):
    global result_Q
    testcases = att.question.question_testcase.all()
    wrapper = att.language.wrapper.path
    source = save_text_to_file(att.source, att.filename)
    permissions = 'chmod u+x {} ;\n'.format(wrapper)
    remarks, results = [], []
    timeout = att.language.timeout * att.question.contest.timeout

    for tst in test_cases:
        inp = tst.inp.path
        out = tst.out.path
        command = ' '.join((permissions, wrap, inp, source))

        ret_val, out_rec, remark = run_command(command, timeout)
        result = get_result(ret_val, out, out_rec)

        results.append(result)
        remarks.append(remark)
    if all([i == 'Correct' for i in results]):
        res = True
        remark = 'All test cases passed.'
    else:  # not everything was correct
        if any([i == 'Timeout' for i in results]):
            res = None
            remark = 'Timeout experienced'
        else:
            res = False
            remark = 'Wrong output'
    result_Q.put((att.pk, res, remark))

def run_command(cmd, timeout):
    class Timeout(Exception):
        pass

    def alarm_handler(signum, frame):
        "Raise the alarm of timeout"
        raise Timeout()

    proc = subprocess.Popen(cmd, stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE, shell=True)
    signal.signal(signal.SIGALARM, alarm_handler)
    signal.alarm(timeout)
    try:
        stdout, stderr = proc.communicate()
        signal.alarm(0)  # reset when command finishes
    except Timeout:
        proc.terminate()
        ret_val = None
        stdout, stderr = b'', b''
    else:
        ret_val = proc.returncode
    return ret_val, stdout.decode(), stderr.decode()

def get_result(return_val, out, out_rec, strict=True):
    result = 'Techincal Difficulty'
    if return_val is None:
        result = 'Timeout'
    elif isinstance(return_val, int):
        if return_val != 0:
            result = 'Error ' + str(return_val)
        else:
            if compare_outputs(out, out_recieved, strict):
                result = 'Correct'
            else:
                result = 'Incorrect'
    return result


def compare_outputs(exp, rec, strict):
    global ERR
    with open(exp, 'r') as e:
        exp = f.read()
    if strict:
        result = exp.strip() == rec.strip()
    else:
        lines_e, lines_r = exp.split('\n'), rec.split('\n')
        result = True
        for e, r in zip(lines_e, lines_r):
            e, r = eval(e), eval(r)
            if abs(e - r) >= ERR:
                result = False
                break
    return result
