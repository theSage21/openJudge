from socket import create_connection
from django.conf import settings
from json import loads, dumps
from random import choice

job_assignment = {}


def ask_check_server(data):
    """
    Ask the check server is the current attempt done?
    Returns True/False and comments.
    data is of type
        data = {
            'pk':primary key of attempt,
            'qno':question number,
            'source':source code url,
            'language':language pk
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
        resp = loads(resp.decode())
        sock.close()
        # return response and remarks
        if resp == 'Timeout':
            return False, resp
        elif resp == 'Correct':
            return True, resp
        elif resp == 'Incorrect':
            return False, resp
