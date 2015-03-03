import os
import time
from django.contrib.auth.models import User
def read(fn):
    f=open(fn,'r')
    lines=f.readlines()
    f.close()
    return ''.join(lines).strip()
def clean_file(filename):
    """Opens a file and removes trailing things from it and writes it back"""
    lines=read(filename)
    f=open(filename,'w')
    f.writelines(lines.strip())
    f.close()
def check_output(f1,f2):
    try:
        lines1=read(f1).split('\n')
        lines2=read(f2).split('\n')
        for i in range(len(lines2)):
            a=lines1[i]
            b=lines2[i]
            a,b=float(a),float(b)
            if abs(a-b)>1e-5:return False
    except:
        return False
    return True
class CheckServer:
    def __init__(self,codepath,testpath,language,attemptid):
        print('Spinning up a check server')
        self.code=codepath
        self.test=testpath
        self.lang=language
        self.attemptid=attemptid
    def run(self):
        wrapper=self.lang.strip()
        arguments=' '.join([self.code.strip(),self.test.strip()])
        pre='chmod u+x '+self.code.strip()+';'
        pre+='chmod u+x '+wrapper+';'
        command=(' '.join([pre,wrapper,arguments]))
        exit_code=os.system(command+'>'+str(self.attemptid))
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
            else:return False,'Output does not match the test case output'
