import os
from socket import create_connection
from django.conf import settings
import json

def ask_check_server(data):
    """ask the check server is the current attempt done?
    Returns True/False and comments.
    If not yet done returns None
    ==============================
    data is of type
        data={
            'pk':primary key of attempt,
            'qno':question number,
            'source':source code url,
            'language':language pk
            }
    """
    address=settings.CHECK_SERVER_ADDRESS
    #create socket
    #send data to check server
    sock=create_connection(address)
    sock.sendall(data.encode('utf-8'))
    #recieve response
    resp=sock.recv(4096)
    resp=json.loads(resp.decode())
    response=resp['response']
    remarks=resp['remarks']
    sock.close()
    #return response and remarks
    if response==None: return None
    else: return response,remarks
