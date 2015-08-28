import sys
import logging
from datetime import datetime
from json import loads, dumps
from socket import socket, SO_REUSEADDR, SOL_SOCKET
from . import config
from . import errors
from . import utils


bcolors = utils.bcolors


def create_log(name, loglevel):
    """
    Taken from:
    stackoverflow.com/questions/14058453/making-python-loggers-output-all-messages-to-stdout-in-addition-to-log#answer-14058475
    """
    root = logging.getLogger(name)
    root.setLevel(loglevel)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    return root


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
                 detail_url=None,
                 listen_addr=None,
                 timeout_limit=None,
                 loglevel=None):
        """
        Arguments:
            webserver       :   address of the webserver
            detail_url    :   the url where language and question details are found
            listen_addr     :   where does this slave listen
            timeout_limit   :   how long to wait before declaring a timout (seconds)
            loglevel        :   Logging level. default is in config=logging.INFO

        After creating a slave call:
            slave.run()
            slave = Slave()
        """
        # set defaults in case missing
        if webserver is None:
            webserver = config.webserver
        if detail_url is None:
            detail_url = config.detail_url
        if listen_addr is None:
            listen_addr = config.listen_addr
        if timeout_limit is None:
            timeout_limit = config.timeout_limit
        if loglevel is None:
            loglevel = config.default_loglevel
        # defaults set
        self.name = config.job_list_prefix + str(listen_addr[1])  # name of slave listening at assigned port
        self.log = create_log('slave_' + str(listen_addr[1]), loglevel)
        self.log.info('Waking up the slave at: ' + str(datetime.now()))
        self.log.debug('Assigning variables')
        self.addr = listen_addr
        self.web = webserver
        self.detail_url = detail_url
        self.timeout_limit = timeout_limit
        self.log.debug('Creating socket')
        self.sock = socket()
        self.log.debug('Socket created.')
        self.job_list = self.__load_jobs()
        # ----------------------
        self.log.debug('Setting socket options')
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind(self.addr)
        self.sock.listen(5)
        self.log.debug('Socket ready to recieve data')
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
        self.log.debug('Loading job info from file')
        try:
            with open(self.name, 'r') as fl:
                data = loads(fl.read())
        except:
            self.log.debug('Jobfile not found, starting afresh')
            data = {}
        self.log.debug('Job data loading complete')
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
        self.log.debug('Closing socket')
        # close comms
        self.sock.close()
        # save job list
        self.log.debug('Saving joblist')
        with open(self.name, 'w') as fl:
            data = dumps(self.job_list)
            fl.write(data)
        self.log.debug('Job list saved')
        self.log.info('Shutdown completed at: ' + str(datetime.now()))

    def __setup(self):
        """
        Obtain language data and question data
        form the webserver at the language_url

        Save in check_data_folder
        return a dict of relevant data
        """
        url = config.protocol_of_webserver + self.web + self.detail_url
        self.log.debug('Getting url for setup')
        try:
            data = utils.get_json(url)
        except errors.InterfaceNotRunning as e:
            self.shutdown('Interface not running: ' + str(e))
            return None
        self.log.debug('JSON for check_data obtained')
        base_url = config.protocol_of_webserver + self.web
        self.log.debug('Getting question details')
        for q in data['question'].keys():
            # input file
            url = base_url + data['question'][q]['inp']
            data['question'][q]['inp'] = utils.get_file_from_url(url, 'inputs')
            # output file
            url = base_url + data['question'][q]['out']
            data['question'][q]['out'] = utils.get_file_from_url(url, 'outputs')
            self.log.debug(q)
        for l in data['language'].keys():
            url = base_url + data['language'][l]['wrap']
            data['language'][l]['wrap'] = utils.get_file_from_url(url, 'wrappers')
            self.log.debug(l)
        self.log.debug('Setup completed')
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
        self.log.debug('Getting source code from webserver')
        source = utils.get_file_from_url(url, 'source', overwrite)
        self.log.debug('Obtained')

        permissions_modifier = 'chmod u+x ' + wrap + ';\n'
        self.log.info('Generating command:')
        command = ' '.join((permissions_modifier, wrap, inp, source))
        self.log.debug(command)
        # ---------------------------------------
        self.log.info('Executing obtained source code')
        return_val, out_recieved, stderr = utils.run_command(command, self.timeout_limit)
        self.log.info('Completed')
        result = utils.get_result(return_val, out, out_recieved)
        remarks = stderr
        self.log.info(remarks)
        self.log.info('-----------------------------------------')
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
