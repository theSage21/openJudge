from subprocess import (run, PIPE, TimeoutExpired)
from .utils import random_string, normalize
from datetime import datetime
import os


class TestCase:
    """
    This is an individual test case.


        t = TestCase(i, o, 10)
        status, out, err = t(code)
    """
    def __init__(self, inp, out, time_limit):
        self.inp = inp
        self.out = out
        self.time_limit = time_limit

    def __call__(self, attempt):
        """Run command on this input and produce verdict"""
        ipath = os.path.join(attempt.workspace, random_string())
        with open(ipath, 'w') as fl:
            fl.write(self.inp)
        cmd = attempt.wrapper.format(input_file=ipath,
                                     code_file=attempt.codepath)
        try:
            p = run(cmd, timeout=self.time_limit,
                    stderr=PIPE, stdout=PIPE,
                    shell=True)
        except TimeoutExpired:
            result = False
            stdout, stderr = b'', b'Timeout'
        else:
            stdout, stderr = p.stdout, p.stderr
            result = p.returncode == 0
            result = result and stdout.decode().strip() == self.out.strip()
        return result, stdout.decode(), stderr.decode()


class Question:
    """
    A single question in some contest.

        q = Question(statement, tests)
        status, log = q(attempt)
    """
    def __init__(self, qno=None, statement=None, test_cases=None):
        self.statement = statement
        self.test_cases = test_cases
        self.qno = qno
        self.qid = random_string()

    def __call__(self, attempt):
        """Run this attempt on this question"""
        log = [test(attempt) for test in self.test_cases]
        status = all([i[0] for i in log])
        attempt.status = status
        attempt.log = log
        return attempt


class Attempt:
    """
    This defines an attempt on some question
    """
    def __init__(self, code=None, wrapper=None, workspace=None,
                 user=None, qid=None):
        """
            a = Attempt(code, wrap, './work/abc')


            code        : The string of the program which it needs to work
            wrap        : The wrapper of the program which makes it work
            workspace   : The common workspace where this attempt is stored
        """
        self.code = code
        self.user = normalize(user) if user is not None else None
        self.qid = qid
        self.wrapper = wrapper
        self.attid = random_string(100)
        self.workspace = None
        self.codepath = None
        self.datetime = datetime.utcnow()
        if workspace is not None:
            wk = os.path.join(workspace, random_string())
            while os.path.exists(wk):
                wk = os.path.join(workspace, random_string())
            self.workspace = wk
            os.mkdir(self.workspace)
            self.codepath = os.path.join(self.workspace, random_string())
            with open(self.codepath, 'w') as fl:
                fl.write(self.code)
