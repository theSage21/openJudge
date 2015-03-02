import os
import time
from django.contrib.auth.models import User

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
        print('------------------------------------')
        print(self.attemptid)
        print(' '.join([pre,wrapper,arguments]))
        print('------------------------------------')
