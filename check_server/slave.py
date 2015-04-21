import os
import time
import json
from socket import *

def read(fn,strip=True):
    f=open(fn,'r')
    lines=f.readlines()
    f.close()
    if strip: return ''.join(lines).strip()
    else:return ''.join(lines)
def clean_file(filename):
    """Opens a file and removes trailing things from it and writes it back"""
    lines=read(filename)
    f=open(filename,'w')
    f.writelines(lines.strip())
    f.close()
def is_alive(pid):
    """Checks if a process is alive"""
    res=os.system('ps -e | grep '+str(pid))
    if res==0:return True
    elif res==256:return False
    else:return None
def check_output(f1,f2,error=True):
    "If error=True check for numerical values with error margins"
    try:
        lines1=read(f1).split('\n')
        lines2=read(f2).split('\n')
        for i in range(len(lines2)):
            a=lines1[i]
            b=lines2[i]
            if error:
                a,b=float(a),float(b)
                if abs(a-b)>1e-5:return False
            else:
                return a==b
    except:
        return False
    return True

class CheckSlave:
    """The slave which checks the attempt.
    A new checkslave is created for each attempt and is killed
    after the attempt has been checked"""
    def __init__(self,master_address,name):
        """Receive an attempt id,
        codepath: absolute path to the code
        testpath: absolute path to test files
        wrapper: absolute path to the required wrapper
        """
        print('Gave birth to a slave.')
        print('Slave id: ',name)
        self.master=master_address
        self.name=name
        #for internal communications
        self.sock=socket()
        pid=os.fork()
        self.pid=pid
        if pid==0:#child
            self.stature='worker'
            self.sock.connect(('127.0.0.1',8888))
        else:#parent
            self.stature='comms'
            self.sock.bind(('127.0.0.1':8888))
            self.accept(5)
            self.comms,adr=self.sock.accept()
            self.sock.close()
            self.sock=socket()
            self.__connect_to_master()
            self.jobs={}
    def __connect_to_master(self):
        self.sock.connect(self.master)
        self.sock.sendall(('Slave name: '+str(self.name)).encode('utf-8'))
        data=self.sock.recv(512)
        if data.decode()!='Registered':
            print('I cannot connect to master. Here is what i recieved:\n',data.decode(),'-'*40)
    def __new_job(self):
        while True:
            #recieve new job
            d=self.sock.recv(4096)
            #send update to master
            self.sock.sendall(json.dumps(self.jobs).encode('utf-8'))
            d=json.loads(d.decode())
            if d['pk'] not in self.jobs.keys(): return d
    def __dispatch_job_to_worker(self,job):
        "For comms"
        data=self.__new_job()
    def __get_and_do_job(self):
        "For worker"
        #get new job
        #do job
        #prepare the command line statements
        wrapper=wrapper.strip()
        arguments=' '.join([code.strip(),test_path.strip()])
        pre='chmod u+x '+code.strip()+';'
        pre+='chmod u+x '+wrapper+';'
        command=(' '.join([pre,wrapper,arguments]))
        #execute the command
        exit_code=os.system(command+'>'+str(self.attemptid))
        #check the exit code
        if exit_code!=0:
            #check the error logs
            lines=read(str(self.attemptid))
            os.system('rm '+str(self.attemptid))
            return False,lines
        else:
            #check outputs
            #rewrite the files to have same length
            clean_file('temp_output')
            clean_file('temp_output_file')
            out=check_output('temp_output','temp_output_file')
            if out:return True,None
            else:return False,'Output does not match the test case output.'
        os.kill(os.getpid(),1)
