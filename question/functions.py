import os
import time
from django.contrib.auth.models import User
def clean_file(filename):
    """Opens a file and removes trailing things from it and writes it back"""
    f=open(filename,'r')
    lines=''.join(f.readlines())
    f.close()
    f=open(filename,'w')
    f.writelines(lines.strip())
    f.close()
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
            f=open(str(self.attemptid),'r')
            lines=''.join(f.readlines())
            f.close()
            os.syatem('rm '+str(self.attemptid))
            return False,lines
        else:
            #check outputs
            #rewrite the files to have same length
            clean_file('temp_output')
            clean_file('temp_output_file')
            diff=os.system('cmp temp_output temp_output_file')
            print(diff)
            if diff==0:return True,None
            else:return False,'Output does not match the test case output'
            
