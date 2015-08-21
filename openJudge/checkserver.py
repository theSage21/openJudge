import os
from random import sample
from json import loads, dumps
from socket import socket, SO_REUSEADDR, SOL_SOCKET
from urllib.request import urlopen, urlretrieve


def get_random_string(l=10):
    return ''.join(sample('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', l))


def get_file_from_url(url, folder, overwrite=False):
    "Get file from url. Overwrite if overwrite-True"
    # create storage path
    path = os.path.join('check_data', folder)
    if not os.path.exists(path):
        os.makedirs(path)
    # get file name
    filename = url.split('/')[-1]
    if not overwrite and os.path.exists(filename):
        salt = get_random_string()
        filename = salt + filename
    # get resources
    complete_path = os.path.join(path, filename)
    fl_name, _ = urlretrieve(url, complete_path)
    return os.path.join(os.getcwd(), fl_name)


def get_json(url):
    "Get json from url and return dict"
    page = urlopen(url)
    text = page.read().decode()
    data = loads(text)
    return data


def is_alive(pid):
    "Check if process is alive"
    # UNIX centric hack. Improve and make cross platform.
    try:
        os.kill(pid, 0)
    except os.ProcessLookupError:
        return False
    else:
        return True


def check_execution(out_expected, outfile, check_error=None):
    "Check if output is correct."
    # get output files
    print(out_expected)
    print(outfile)
    with open(out_expected, 'r') as f:
        lines_expected = f.readlines()
    with open(outfile, 'r') as f:
        lines_got = f.readlines()
    print(lines_expected)
    print(lines_got)
    # check line by line
    for got, exp in zip(lines_got, lines_expected):
        if check_error is None:  # exact checking
            if exp.strip() != got.strip():
                return False
        else:  # error range checking
            if abs(eval(exp.strip()) - eval(got.strip())) > eval(check_error):
                return False
    return True


class Slave:
    def __init__(self,
                 webserver='127.0.0.1:8000',  # where is the webserver
                 language_url='/question/detail_list/',  # what us the language data url
                 listen_addr=('127.0.0.1', 9000),  # where should this slave listen
                 timeout_limit=30  # how long to wait for timeout?
                 ):
        self.name = 'joblist_' + listen_addr[1]  # name of slave listening at assigned port
        print('Waking up the slave')
        self.addr = listen_addr
        self.web = webserver
        self.lang_url = language_url
        self.timeout_limit = timeout_limit
        self.processes = []
        self.sock = socket()
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind(self.addr)
        self.sock.listen(5)
        print('The slave is learning about the contest.')
        self.check_data = self.__setup()
        print('Slave awaiting orders at: ', self.sock.getsockname())
        self.job_list = self.__load_jobs()

    def __load_jobs(self):
        "Load jobs according to self name"
        with open(self.name, 'r') as fl:
            data = loads(fl.read().decode())
        return data

    def __shutdown(self):
        # kill existing jobs
        print('Abandoning all running checks')
        for i in self.processes:
            os.kill(i, 1)
        print('Cutting all communications')
        # close comms
        self.sock.close()
        # save job list
        with open(self.name, 'w') as fl:
            data = dumps(self.job_list)
            fl.write(data)

    def __setup(self):
        "Obtain language data and question data"
        url = 'http://' + self.web + self.lang_url
        data = get_json(url)
        print('Questions obtained:')
        for q in data['question'].keys():
            # input file
            url = 'http://' + self.web + data['question'][q]['inp']
            data['question'][q]['inp'] = get_file_from_url(url, 'inputs')
            # output file
            url = 'http://' + self.web + data['question'][q]['out']
            data['question'][q]['out'] = get_file_from_url(url, 'outputs')
            print(q)
        print('Languages obtained')
        for l in data['language'].keys():
            url = 'http://' + self.web + data['language'][l]['wrap']
            data['language'][l]['wrap'] = get_file_from_url(url, 'wrappers')
            print(l)
        return data

    def __process_request(self, data):
        # TODO: check if question exists in case someone is malicious
        # setup
        print('Prepping for check')
        lang, qno = str(data['language']), str(data['qno'])

        wrap = self.check_data['language'][lang]['wrap']
        inp = self.check_data['question'][qno]['inp']
        out = self.check_data['question'][qno]['out']

        overwrite = self.check_data['language'][lang]['overwrite']
        url = 'http://' + self.web + data['source']
        source = get_file_from_url(url, 'source', overwrite)

        outfile = 'check_data/temp/OUT_' + get_random_string()

        permissions_modifier = 'chmod u+x ' + wrap + ' && \n'
        print('Generating command:')
        command = ' '.join((permissions_modifier, wrap, inp, source, outfile))
        print(command)
        # ---------------------------------------
        print('Executing')
        return_val = os.system(command)
        if return_val != 0:
            print('ERROR: Return value non zero: ', return_val)
        # TODO:implement timeout mechanism
        """
        else:
            start = time.time()
            while is_alive(pid):
                if time.time() - start > self.timeout_limit:
                    os.kill(pid, 1)
                    return 'Timeout'
                else:
                    time.sleep(1)
        """
        if return_val == 0:
            if check_execution(out, outfile):
                result = 'Correct'
            else:
                result = 'Incorrect'
        else:
            result = 'Incorrect'
        print(result)
        print('-' * 50)
        return result

    def run(self):
        while True:
            try:
                com, ard = self.sock.accept()
                data = com.recv(4096)
                data = loads(data.decode())
                if data['pk'] not in self.job_list.keys():  # First time for processing
                    result = self.__process_request(data)
                    self.job_list[data['pk']] = result  # add to joblist
                    result = dumps(result)
                else:  # not first time
                    result = dumps(self.job_list[data['pk']])
                com.sendall(result.encode('utf-8'))
                com.close()
            except KeyboardInterrupt:
                print('The slave is retiring')
                self.__shutdown()
                print('The slave is dead.')

if __name__ == '__main__':
    sl = Slave()
    sl.run()
