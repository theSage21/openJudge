import os
from urllib.request import urlopen

class DB:
    def __init__(self,path=None):
        """A database to store attempt details"""
        if path==None:self.path=os.getcwd()
        else:self.path=path
        self.index={}
        self.load()
    def save(self):
    def load(self):
    def update_attempt(self,attid,data):
    def __save_from_url(self,base_addr,url,sub_id=None):
        "Returns the absolute path of the saved file"
    def check_status(self,attid):
        "Return the check status of an attempt"
        return None
    def add_attempt(self,data):
        self.index['attempt'][str(data['pk'])]={'qno':data['qno'],
                                                'source':self.__save_from_url(base,data['source'],data['pk'])
                                                'language':data['language']
                                                'status':None,
                                                'remarks':'Checking'
                                                }
        self.save()
    def get_attempt(self,attempt_id,detail=None):
        "returns required details from attempts"
        attempt_id=str(attempt_id)
        if attempt_id in self.index['attempt'].keys():
            if detail==None:return self.index['attempt'][attempt_id]
            else:
                try:
                    data=self.index['attempt'][attempt_id][detail]
                except Exception as e:
                    print('Error in database')
                    print('-'*20)
                    print(e)
                    print('-'*20)
                else:
                    return data
    def contains_attempt(self,attid):
        return str(attid) in self.index['attempt']
    def update_check_details(self,data):
        self.index.update(data)
