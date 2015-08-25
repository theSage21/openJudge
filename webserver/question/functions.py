from socket import create_connection
from django.conf import settings
from json import loads, dumps
from random import choice
from question.models import Attempt


def ask_check_server(data,
                     job_assignment={},  # for keeping track of jobs
                     ):
    """
    Ask the check server is the current attempt done?
    Returns None/True/False and comments.
    data is of type
        data = {
            'pk'        :primary key of attempt,
            'qno'       :question number pk,
            'source'    :source code url,
            'language'  :language pk
            }
    """
    if data['pk'] not in job_assignment.keys():
        job_assignment[data['pk']] = choice(settings.SLAVE_ADDRESSES)
    address = job_assignment[data['pk']]
    # create socket
    # send data to check server
    try:
        sock = create_connection(address)
    except:
        return None, 'Connection error'
    else:
        data = dumps(data)
        sock.sendall(data.encode('utf-8'))
        # recieve response
        resp = sock.recv(4096)
        resp, remarks = loads(resp.decode())
        sock.close()
        # return response and remarks
        if resp == 'Timeout':
            return False, resp
        elif resp == 'Correct':
            return True, resp
        elif resp == 'Incorrect':
            return False, resp
        elif resp == 'Error':
            return False, remarks


def is_correct(attempt):
    """Checks if the attempt was correct
    By contacting the check server."""
    if attempt.correct is not None:
        return attempt.correct
    else:
        data = attempt.get_json__()
        result, comment = ask_check_server(data)
        if result is not None:
            attempt.correct = result
            attempt.remarks = comment
            attempt.marks = get_marks(attempt.question)
            attempt.save()
            return attempt.correct


def get_marks(question):
    """Get the current score for a question"""
    total_attempts = Attempt.objects.filter(question=question).exclude(correct=None).count()
    wrong_attempts = Attempt.objects.filter(question=question, correct=False).count()
    if total_attempts == 0:
        score = 1.0
    else:
        score = float(wrong_attempts) / float(total_attempts)
    return score


def update_marks(profile, attempt):
    correct_attempts = Attempt.objects.filter(player=profile,
                                              question=attempt.question,
                                              correct=True,
                                              ).exclude(pk=attempt.pk).count()
    if correct_attempts < 1:  # this has never been correctly attempted
        if attempt.correct:
            profile.score += attempt.marks
            profile.save()
