import os
import logging
import signal
import subprocess
from random import sample
from . import config, errors
from urllib.request import urlretrieve, urlopen
from urllib.error import URLError
from json import loads


logging.basicConfig(filename=config.logfile,
                    level=config.default_loglevel)
log = logging.getLogger('utils')


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
    elif isinstance(return_val, int):
        if return_val != 0:
            result = 'Error'
        else:
            if check_execution(out, out_recieved):
                result = 'Correct'
            else:
                result = 'Incorrect'
    log.info(result)
    return result


def get_random_string(l=10):
    "Returns a string of random alphabets of 'l' length"
    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alpha += alpha.lower()
    if l > 26*2:
        alpha = alpha * (int(l/(26*2)) + 1)
    return ''.join(sample(alpha, l))


def get_file_from_url(url, folder, overwrite=False):
    """Get file from url.
    Store in provided folder.
    Overwrite if overwrite=True"""
    # create storage path
    path = os.path.join(config.check_data_folder, folder)
    if not os.path.exists(path):
        log.debug('Path did nto exist. Was created. ' + path)
        os.makedirs(path)
    # get file name
    filename = url.split('/')[-1]
    filepath = os.path.join(path, filename)
    if not overwrite and os.path.exists(filepath):
        log.debug('Salting the file')
        salt = get_random_string()
        filename = salt + filename
    # get resources
    complete_path = os.path.join(path, filename)
    try:
        fl_name, _ = urlretrieve(url, complete_path)
    except URLError:
        log.debug('Unable to retrieve url(file_from_url): {}'.format(url))
        raise errors.InterfaceNotRunning('URL unavailable: {}'.format(url))
    return os.path.join(os.getcwd(), fl_name)


def save_text_to_file(text, file_path, overwrite=False):
    path, name = os.path.split(file_path)
    if not overwrite and os.path.exists(file_path):
        log.debug('Salting the file name')
        salt = get_random_string()
        name = salt + name
        file_path = os.path.join(path, name)
        log.debug('Done')
    with open(file_path, 'w') as fl:
        fl.write(text)
    return file_path


def get_json(url):
    "Get json from url and return dict"
    try:
        page = urlopen(url)
    except URLError:
        log.debug('Unable to retrieve url(getjson): {}'.format(url))
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
    log.debug('Opening output_expected file')
    with open(out_expected, 'r') as f:
        lines_expected = f.readlines()
    log.debug('Expected output recieved')
    lines_got = out_recieved.split('\n')
    # check line by line
    log.debug('Starting coparison')
    result = True
    for got, exp in zip(lines_got, lines_expected):
        if check_error is None:  # exact checking
            if exp.strip() != got.strip():
                log.debug('Inequality found:' + exp.strip() + ' != ' + got.strip())
                result = False
                break
        else:  # error range checking
            if abs(eval(exp.strip()) - eval(got.strip())) > check_error:
                log.debug('Inequality found:' + exp.strip() + ' != ' + got.strip())
                result = False
                break
    log.debug('Check completed: ' + str(result))
    return result


def run_command(cmd, timeout=config.timeout_limit):
    """
    Run the command in a subprocess and wait for timeout
    time before killing it.
    Errors are recorded and output is recorded"""
    def alarm_handler(signum, frame):
        "Raise the alarm of timeout"
        raise errors.Timeout
    log.debug('Starting subprocess')

    proc = subprocess.Popen(cmd,
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            shell=True
                            )

    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(timeout)
    try:
        stdoutdata, stderrdata = proc.communicate()
        log.debug('Subprocess ended')
        signal.alarm(0)  # reset the alarm
    except errors.Timeout:
        log.debug('Timeout experienced')
        proc.terminate()
        ret_val = None
        stderrdata = b''
        stdoutdata = b''
    else:
        ret_val = proc.returncode
    log.debug('Subprocess completed with result: ' + str(ret_val))
    return ret_val, stdoutdata.decode(), stderrdata.decode()
