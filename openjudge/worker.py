from multiprocessing import Pool
from time import sleep
from .core import Attempt, Question, TestCase
import pymongo
import random


def _attempt_checker(mongo_uri):
    db = pymongo.MongoClient(mongo_uri)
    db = db.openjudge
    while True:
        attempt = db.attempt_queue.find_one_and_delete({})
        if attempt is None:
            sleep(random.random())
        else:
            att = Attempt()
            att.__dict__ = attempt
            # has this been answered correctly earlier?
            query = {"qid": att.qid, "user": att.user,
                     "status": True}
            if db.history.find_one(query) is None:
                q = db.questions.find_one({"qid": att.qid})
                que = Question()
                que.__dict__ = q
                que.test_cases = [TestCase(**t) for t in q['test_cases']]
                checked_attempt = que(att)
            else:
                att['status'] = False
                att['log'] = None
                checked_attempt = att
            db.history.insert_one(checked_attempt.__dict__)


def run_judge(mongo_uri, n_judges):
    with Pool() as pool:
        args = [mongo_uri for _ in range(n_judges)]
        pool.map(_attempt_checker, args)
