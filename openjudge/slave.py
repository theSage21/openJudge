import os
import signal
import subprocess
import logging
from datetime import datetime
from random import sample
from json import loads, dumps
from socket import socket, SO_REUSEADDR, SOL_SOCKET
from urllib.request import urlopen, urlretrieve
from urllib.error import URLError
from . import config
from . import errors
from . import utils


bcolors = utils.bcolors
logging.basicConfig(filename=config.logfile,
                    level=logging.DEBUG)
judge_log = logging.getLogger('judge')


def get_result(return_val, out, out_recieved):
    """
    Based on return value provided,
             output recieved,
             output expected
    return a result which is in
            [Timeout, Correct, Incorrect, Error, <catchall>]
    along with a remark pertaining to the case.
    """
    result = 'Contact a volunteer'
    if return_val is None:
        result = 'Timeout'
        judge_log.info(result)
    elif isinstance(return_val, int):
        if return_val != 0:
            judge_log.info('ERROR: Return value non zero: ' + return_val)
            result = 'Error'
            judge_log.info(result)
        else:
            if check_execution(out, out_recieved):
                result = 'Correct'
                judge_log.info(result)
            else:
                result = 'Incorrect'
                judge_log.info(result)
    return result


def get_random_string(l=10):
    "Returns a string of random alphabets of 'l' length"
    return ''.join(sample('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', l))


def get_file_from_url(url, folder, overwrite=False):
    "Get file from url. Overwrite if overwrite=True"
    # create storage path
    path = os.path.join(config.check_data_folder, folder)
    if not os.path.exists(path):
        os.makedirs(path)
    # get file name
    filename = url.split('/')[-1]
    filepath = os.path.join(path, filename)
    if not overwrite and os.path.exists(filepath):
        salt = get_random_string()
        filename = salt + filename
    # get resources
    complete_path = os.path.join(path, filename)
    try:
        fl_name, _ = urlretrieve(url, complete_path)
    except URLError:
        raise errors.InterfaceNotRunning('URL unavailable: {}'.format(url))
    return os.path.join(os.getcwd(), fl_name)


def get_json(url):
    "Get json from url and return dict"
    try:
        page = urlopen(url)
    except URLError:
        raise errors.InterfaceNotRunning('URL unavailable: {}'.format(url))
    text = page.read().decode()
    data = loads(text)
    return data


def check_execution(out_expected, out_recieved, check_error=None):
    """Check if output is correct.
    Output is checked against expected output.
    There are two methods of checking.
        - Exact      : String comparison is made
        - Error range: Difference must be within error range
    """
    # get output files
    with open(out_expected, 'r') as f:
        lines_expected = f.readlines()
    lines_got = out_recieved.split('\n')
    # check line by line
    for got, exp in zip(lines_got, lines_expected):
        if check_error is None:  # exact checking
            if exp.strip() != got.strip():
                return False
        else:  # error range checking
            if abs(eval(exp.strip()) - eval(got.strip())) > check_error:
                return False
    return True


def run_command(cmd, timeout=config.timeout_limit):
    """
    Run the command in a subprocess and wait for timeout
    time before killing it.
    Errors are recorded and output is recorded"""
    def alarm_handler(signum, frame):
        "Raise the alarm of timeout"
        raise errors.Timeout

    proc = subprocess.Popen(cmd,
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            shell=True
                            )

    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(timeout)
    try:
        stdoutdata, stderrdata = proc.communicate()
        signal.alarm(0)  # reset the alarm
    except errors.Timeout:
        proc.terminate()
        ret_val = None
        stderrdata = b''
        stdoutdata = b''
    else:
        ret_val = proc.returncode
    return ret_val, stdoutdata.decode(), stderrdata.decode()


class Slave:
    """
    The slave class is the main class in the check slave.

    It does the following:
        - Setup itself with information about the contest
        - Recieve jobs on a listening address
        - Perform check for jobs
        - Return the result of the checks
        - Remember checked jobs.
    """
    def __init__(self,
                 webserver=None,
                 language_url=None,
                 listen_addr=None,
                 timeout_limit=None):
        """
        Arguments:
            webserver       :   address of the webserver
            language_url    :   the url where language and question details are found
            listen_addr     :   where does this slave listen
            timeout_limit   :   how long to wait before declaring a timout (seconds)

        After creating a slave call:
            slave.run()
            slave = Slave()
        """
        # set defaults in case missing
        if webserver is None:
            webserver = config.webserver
        if language_url is None:
            language_url = config.language_url
        if listen_addr is None:
            listen_addr = config.listen_addr
        if timeout_limit is None:
            timeout_limit = config.timeout_limit
        # defaults set
        self.name = config.job_list_prefix + str(listen_addr[1])  # name of slave listening at assigned port
        self.log = logging.getLogger('slave_' + str(listen_addr[1]))
        self.log.info('Waking up the slave at: ' + str(datetime.now()))
        self.addr = listen_addr
        self.web = webserver
        self.lang_url = language_url
        self.timeout_limit = timeout_limit
        self.sock = socket()
        self.job_list = self.__load_jobs()
        # ----------------------
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind(self.addr)
        self.sock.listen(5)
        self.log.info('The slave is learning about the contest.')
        data = self.__setup()
        if data is None:
            self.log.error('Setup failed')
            return
        self.check_data = data
        self.log.info('Slave awaiting orders at: ' + str(self.sock.getsockname()))

    def __load_jobs(self):
        """
        Load jobs according to self.name
        If none exist return an empty job dictionary
        """
        try:
            with open(self.name, 'r') as fl:
                data = loads(fl.read())
        except:
            self.log.info('Jobfile not found, starting afresh')
            data = {}
        return data

    def shutdown(self, reason='Direct call'):
        """
        Cleanly shutdown the slave.
        - Close sockets
        - Kill existing jobs
        - Save joblist
        """
        self.log.info('Shutting down due to: ' + reason)
        # kill existing jobs
        self.log.info('Cutting all communications')
        # close comms
        self.sock.close()
        # save job list
        self.log.info('Saving joblist')
        with open(self.name, 'w') as fl:
            data = dumps(self.job_list)
            fl.write(data)
        self.log.info('Job list saved')
        self.log.info('Shutdown completed at: ' + str(datetime.now()))

    def __setup(self):
        """
        Obtain language data and question data
        form the webserver at the language_url

        Save in check_data_folder
        return a dict of relevant data
        """
        url = config.protocol_of_webserver + self.web + self.lang_url
        try:
            data = get_json(url)
        except errors.InterfaceNotRunning as e:
            self.shutdown('Interface not running: ' + str(e))
            return None
        self.log.info('Questions obtained:')
        base_url = config.protocol_of_webserver + self.web
        for q in data['question'].keys():
            # input file
            url = base_url + data['question'][q]['inp']
            data['question'][q]['inp'] = get_file_from_url(url, 'inputs')
            # output file
            url = base_url + data['question'][q]['out']
            data['question'][q]['out'] = get_file_from_url(url, 'outputs')
            self.log.info(q)
        self.log.info('Languages obtained')
        for l in data['language'].keys():
            url = base_url + data['language'][l]['wrap']
            data['language'][l]['wrap'] = get_file_from_url(url, 'wrappers')
            self.log.info(l)
        return data

    def __process_request(self, data):
        """
        Process the request.

        - Check if data is valid
        - Execute the program
        - Collect information
        - Return results

        Print out information during the process

        requires the data to be :
        data = {
                'pk'        :primary key of attempt,
                'qno'       :question number pk,
                'source'    :source code url,
                'language'  :language pk,
                }
        """

        # TODO: check if question exists in case someone is malicious
        # setup
        self.log.info('Prepping for check pk:' + str(data['pk']))
        lang, qno = str(data['language']), str(data['qno'])

        wrap = self.check_data['language'][lang]['wrap']
        inp = self.check_data['question'][qno]['inp']
        out = self.check_data['question'][qno]['out']

        overwrite = self.check_data['language'][lang]['overwrite']
        url = config.protocol_of_webserver + self.web + data['source']
        source = get_file_from_url(url, 'source', overwrite)

        permissions_modifier = 'chmod u+x ' + wrap + ';\n'
        self.log.info('Generating command:')
        command = ' '.join((permissions_modifier, wrap, inp, source))
        self.log.info(command)
        # ---------------------------------------
        self.log.info('Executing')
        return_val, out_recieved, stderr = run_command(command, self.timeout_limit)
        result = get_result(return_val, out, out_recieved)
        remarks = stderr
        self.log.info(remarks)
        return result, remarks

    def run(self):  # pragma: no cover
        """
        Run the slave in an infinite loop of accepting and executing
        requests from the webserver.
        """
        # since this is an infinite loop, we do not test it
        while True:
            try:
                data, com = self.get_data_from_socket()
                result = self.assign_to_job_list(data)
                com.sendall(result.encode('utf-8'))
                com.close()
            except KeyboardInterrupt:
                self.log.info('The slave is retiring')
                self.shutdown('Keyboard interrupt')
                self.log.info('The slave is dead.')
            except OSError:
                break  # the accept call which will raise a traceback

    def get_data_from_socket(self):
        """
        Accepts data sent to it and returns
        the communication point and data
        """
        com, _ = self.sock.accept()
        data = com.recv(4096)
        data = loads(data.decode())
        return data, com

    def assign_to_job_list(self, data):
        """
        Assign to job list or return an already executed result
        """
        if data['pk'] not in self.job_list.keys():  # First time for processing
            self.log.info('Job recieved for first time: ' + str(data['pk']))
            result = self.__process_request(data)
            self.job_list[data['pk']] = result  # add to joblist
            result = dumps(result)
        else:  # not first time
            self.log.info('Job recieved: ' + str(data['pk']))
            result = dumps(self.job_list[data['pk']])
        return result

if __name__ == '__main__':
    sl = Slave()
    sl.run()
