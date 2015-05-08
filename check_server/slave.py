#Call from command line and provide as argument
#the webaddress and the self listening address

import os,time
import json
from socket import *
from urllib.request import urlopen

def get_file_fom_url(url,overwrite=False):
    """Retrieves file from given url and saves to disk.
    returns absolute filepath.
    If overwrite is true overwrites an existing file"""
    page=urlopen(url)
    filename=url.split('/')[-1]
    if os.path.exists(filename) and not overwrite:
        from random import random
        no=str(int(random()*100))
        filename+='_'+no
    f=open(filename,'w')
    f.writelines(page.readlines())
    f.close()
    return os.path.join(os.getcwd(),filename)

def is_alive(pid):
    """Checks if a process is alive. UNIX centric"""
    try: os.kill((pid),0)
    except ProcessLookupError:return False
    else:return True

def result_of_execution(out_expected):
    """Checks if expected and obtained outputs match"""
    f=open(out_expected,'r')
    lines_expected=f.readlines()
    f.close()
    f=open('temp_output','r')
    lines_got=f.readlines()
    f.close()
    for i in range(max(len(lines_expected),len(lines_got))):
        exp=lines_expected[i]
        got=lines_got[i]
        if exp.strip()!=got.strip():return False
    return True

class Slave:
    def __init__(self,webserver,listen_address=('0.0.0.0',9000)):
        print("Anouncing loyalty to the web address")
        self.addr=listen_address
        self.webserver=webserver
        self.__get_question_details()
        #----------
        self.sock=socket()
        self.sock.bind(self.addr)
        self.sock.listen(5)
        print("Slave active at: ",self.sock.getsockname())
        #----------
        self.processes=[]#list of processes created.
    def __get_question_details(self):
        """Gets question details and language wrappers from the webserver"""
        self.check_data={}
        url=self.webserver+'/question/detail_list/'
        url='http://'+url
        #we let the exception fall through
        #as without this nothing works
        page=urlopen(url)
        text=''.join((i.decode() for i in page.readlines()))
        data=json.loads(text)
        #replace urls by filepaths
        for q in data['question'].keys():
            url='http://'+self.webserver+data['question'][q]['inp']
            filename=get_file_from_url(url)
            data['question'][q]['inp']=filename
            url='http://'+self.webserver+data['question'][q]['out']
            filename=get_file_from_url(url)
            data['question'][q]['out']=filename
        for q in data['language'].keys():
            url='http://'+self.webserver+data['language'][q]['wrap']
            filename=get_file_from_url(url)
            data['language'][q]['wrap']=filename
            #Make executable
            os.system('chmod u+x '+filename)
        self.check_data=data
    def __process_request(self,data):
        """Process a request."""
        print(data['pk'])
        lang=data['language']
        qno=data['qno']
        wrap=self.check_data['language'][lang]['wrap']#---
        inp=self.check_data['question'][qno]['inp']#---
        out=self.check_data['question'][qno]['out']#---
        #-----
        overwrite=self.check_data['language'][lang]['overwrite']
        source=get_file_from_url(data['source'],overwrite)#---
        #------create the command line command
        command+=' '.join((wrap,inp,source))
        #------execute the command
        pid=os.fork()
        if pid==0:#child
            os.system(command)
        else:
            start=time.time()
            while is_alive(pid):
                if time.time()-start>30:
                    os.kill(pid,1)
                    return 'Timeout'
                else:time.sleep(1)
            if result_of_execution(out):
                return 'Correct'
            else:return 'Incorrect'
        #--------main thread resumes
    def __recalculate_alive_processes(self):
        """Calculates how many of the processes in self.processes
        are alive. removes the dead ones"""
        alive=[]
        for proc in self.processes:
            if is_alive(proc):alive.append(proc)
        self.processes=alive
    def __print_running_checks(self):
        """Prints the process numbers of running checks"""
        print('|'.join(map(str,self.processes)))
    def run(self):
        self.__recalculate_alive_processes()
        self.__print_running_checks()
        com,adr=self.sock.accept()
        pid=os.fork()#Fork a new check
        if pid==0:
            data=com.recv(4096)
            data=json.loads(data.decode())
            result=self.__process_request(data)
            result=json.dumps(result)
            com.sendall(result.encode('utf-8'))
            com.close()
        else: self.processes.append(pid)

if __name__=='__main__':
    #webaddress=input("Enter webaddress:\nExample: 129.168.1.15:8000\n:- ")
    webaddress='127.0.0.1:8000'
    sl=Slave(webaddress)
    sl.run()
