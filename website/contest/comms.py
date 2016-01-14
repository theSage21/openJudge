import random
from queue import Queue
from threading import Thread
from json import loads, dumps
from contest.models import Slave
from socket import create_connection

joblist = {}
BUFFER = 4096

def is_correct(attempt):
    first_time = is_first_time(attempt)
    allocation_needed = False
    if first_time:
        allocation_needed = True
    else:
        allocated_to = get_allocation(attempt)
        alive_slaves = get_alive_slaves()
        if not allocated_to in alive_slaves:
            allocation_needed = True
    if allocation_needed:
        alive_slaves = get_alive_slaves()
        idle_slave = get_idle_slave(alive_slaves)
        register_allocation(attempt, idle_slave)
    slave = get_allocation(attempt)
    return ask_status(attempt, slave)

def is_first_time(attempt):
    global joblist
    return not (attempt.pk in joblist.keys())


def get_allocation(attempt):
    global joblist
    return joblist[attempt.pk]


def get_alive_slaves():
    slaves = Slave.objects.all()
    return [s for s in slaves if s.is_alive()]


def get_idle_slave(slaves):
    return [i for i in slaves if not i.busy][0]


def register_allocation(attempt, slave):
    global joblist
    joblist[attempt.pk] = slave


def ask_status(attempt, slave):
    data = get_attempt_data(attempt)
    t = Thread(target=ask_slave, args=(slave, data))
    t.start()
    global result_Q
    # wait for result to come or say checking
    results = {}
    while result_Q.qsize() > 0:
        key, val, rem = result_Q.get()
        results[key] = (val, rem)
    pk = data['pk']
    result, comment = None, "Checking..."
    for key, value in results.items():
        if key == pk:
            result, comment = value
        else:
            result_Q.put((key, value[0], value[1]))
    return result


def ask_slave(slave, data):
    global BUFFER
    address = slave.get_address()
    with slave:
        with create_connection(address) as sock:
            data = dumps(data)
            sock.sendall(data.encode('utf-8'))
            resp = sock.recv(BUFFER)
            resp, remarks = loads(resp.decode())
    value, remarks = get_response_mapping(resp, remarks)

def get_attempt_data(attempt):
    data = {'pk': attempt.pk,
            'qno': attempt.question.pk,
            'source': attempt.source,
            'name': attempt.filename,
            'language': attempt.language.pk}
    return data


def get_response_mapping(resp, remarks):
    if resp == 'Timeout':
        value, remarks = False, resp
    elif resp == 'Correct':
        value, remarks = True, resp
    elif resp == 'Incorrect':
        value, remarks = False, resp
    elif resp == 'Error':
        value, remarks = False, remarks
    return value, remarks
