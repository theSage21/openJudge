import os
import random


def random_string(n=15):
    return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz')
                    for _ in range(n)])


def normalize(string):
    return string.lower().strip()


async def add_questions_from_dir(dirname, time_limit, db):
    questions = [(i, os.path.join(dirname, i))
                 for i in os.listdir(dirname)]
    for qno, qpath in questions:
        qno = int(qno)
        q = await db.questions.find_one({"qno": qno})
        if q is None:
            print('Adding a new question', qno)
            q = {"qno": qno, "qid": random_string()}
            with open(os.path.join(qpath, 'statement'), 'r') as fl:
                q['statement'] = fl.read()
            ios = set([i[1:] for i in os.listdir(qpath) if i[0] in 'io'])
            q['test_cases'] = []
            for no in ios:
                tcase = {}
                with open(os.path.join(qpath, 'i'+no), 'r') as fl:
                    tcase['inp'] = fl.read()
                with open(os.path.join(qpath, 'o'+no), 'r') as fl:
                    tcase['out'] = fl.read()
                tcase['time_limit'] = time_limit
                q['test_cases'].append(tcase)
            await db.questions.insert_one(q)
