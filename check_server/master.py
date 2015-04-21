import os
import time
import json
import random
from database import DB
from socket import *
from queue import Queue

class Slave:
    "Slave handle for the master"
    def __init__(self,com,arddr,name):
        self.sock=comm
        self.addr=addr
        self.name=name
        self.jobs={}
    def jobs_done(self):
        return len([1 for i in self.jobs if i.complete()])
    def compute_rate(self):
        total=len(self.jobs.keys())
        done=sum((1 for j in self.jobs.keys() if self.jobs[j]['status']=True))
        return round(float(done)/total,2)
    def get_status(self,att_id):
        return self.jobs[att_id]['status']
    def give_job(self,data):
        self.jobs[data['pk']]=data
        self.jobs[data['pk']]['run_attempt']=1
        self.jobs[data['pk']]['status']=None
        self.sock.sendall(job_data)
        update=self.sock.recv(1024)
        update=json.loads(update.decode())
        #update job status
        self.__update_job_status(update)
    def __update_job_status(self.data):

class CheckMaster:
    """Class to dictate which slaves should check the attempts"""
    def __init__(self,listening_address,web_address,check_timeout=30):
        """Where should this master listen?
        What is the address of webserver
        How long should an attempt take to compile and run?"""
        self.address=listening_address
        self.webserver=web_address
        self.timeout=check_timeout
        self.task_list=Queue()
        #---------
        self.sock=socket()
        self.sock.bind(self.address)
        self.sock.listen(5)
        #-----------
        self.slaves=__get_slaves()
        self.dispatch_register={}
        self.check_details=self.__get_question_and_language_details()
    def __get_slaves(self):
        """Waits for slaves to connect. Asks user if enough slaves have connected"""
        slaves=[]
        while True:
            com,adr=self.sock.accept()
            r=com.recv(4096)
            r=r.decode()
            if 'Slave name:' in r:
                slave=Slave(com,adr,str(len(slaves)))
                slaves.append(slave)
                #acknowledge the slave as registered
                com.sendall('Registered'.encode('utf-8'))
                print('Slave recieved at :',adr)
                if input('All slaves done?(y/n): ')=='y':break
        return slaves
    def __get_question_and_language_details(self):
        "Return JSON of details retrieved.
        In case of any error return None"
        url=self.webserver+'/question/detail_list/'
        try:
            page=urlopen('http://'+url)
        except Exception as e:
            print('Exception in opening url \n',url)
            print('-'*10)
            print(e)
            print('-'*10)
            return None
        else:
            text=''.join((i.decode() for i in page.readlines()))
            data=json.loads(text)
            return data
    def __get_job_data(self,data):
        q_data=self.check_details['question'][data['qno']]
        l_data=self.check_details['language'][data['language']]
        resp_data={}
        resp_data['wrapper']=l_data['wrap']
        resp_data['inp']=q_data['inp']
        resp_data['out']=q_data['out']
        resp_data['type']=q_data['type']
        resp_data['source']=data['source']
        resp_data['pk']=data['pk']
        return resp_data
    def __dispatch_to_slave(self,data):
        pk=data['pk']
        slave=random.choice(self.slaves)
        job_data=self.__get_job_data(data)
        slave.give_job(job_data)
        self.dispatch_register[str(pk)]=slave
    def __read_request(self):
        """Read requests from the webserver
        Data recieved is of format:
            data={
                'pk':primary key of attempt
                'qno':question number attemptd
                'source':url of uploaded source code
                'language':language attempted in
                }
        """
        con,addr=self.sock.accept()
        req=con.recv(4096)
        req=json.loads(req.decode())
        #get details done
        return req,con
    def __process_request(self,req,con):
        att_id=req['pk']
        self.__dispatch_to_slave(req)
        #return a response
        resp=self.dispatch_register[att_id].get_status(att_id)
        resp=json.dumps(resp)
        con.sendall(resp.encode('utf-8'))
        con.close()
    def run(self):
        while True:
            req,con=self.__read_request()
            self.__process_request(req,con)
            status=''
            for s in self.slaves:
                status+=' '+s.name+':'+s.compute_rate()+'|'
            print(status,end='\r')
