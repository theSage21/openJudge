from subprocess import (run, PIPE, TimeoutExpired)
from utils import random_string
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
            result = p.returncode == 0
            stdout, stderr = p.stdout, p.stderr
        return result, stdout.decode(), stderr.decode()


class Question:
    """
    A single question in some contest.

        q = Question(statement, tests)
        status, log = q(attempt)
    """
    def __init__(self, statement, test_cases):
        self.statement = statement
        self.test_cases = test_cases

    def __call__(self, attempt):
        """Run this attempt on this question"""
        log = [test(attempt) for test in self.test_cases]
        return all([i[0] for i in log]), log


class Attempt:
    """
    This defines an attempt on some question
    """
    def __init__(self, code, wrapper, workspace):
        """
            a = Attempt(code, wrap, './work/abc')


            code        : The string of the program which it needs to work
            wrap        : The wrapper of the program which makes it work
            workspace   : The common workspace where this attempt is stored
        """
        self.code = code
        self.wrapper = wrapper
        self.workspace = os.path.join(workspace, random_string())
        self.codepath = os.path.join(self.workspace, random_string())
        with open(self.codepath, 'w') as fl:
            fl.write(self.code)


class Contest:
    def __init__(self, name, questions, running=False):
        self.name = name
        self.questions = questions
        self.running = running
