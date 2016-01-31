import sys

if sys.version_info >= (3, 5):
    from subprocess import (run,
                            PIPE,
                            TimeoutExpired)
    print('V> 3.5')

else:

    from subprocess import (PIPE,
                            Popen,
                            TimeoutExpired,
                            CalledProcessError,
                            CompletedProcess)

    def run(*popenargs, input=None, timeout=None, check=False, **kwargs):
        print('Using custom run')
        if input is not None:
            if 'stdin' in kwargs:
                raise ValueError('stdin and input arguments may not both be used.')
            kwargs['stdin'] = PIPE

        with Popen(*popenargs, **kwargs) as process:
            try:
                stdout, stderr = process.communicate(input, timeout=timeout)
            except TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                raise TimeoutExpired(process.args, timeout, output=stdout,
                                     stderr=stderr)
            except:
                process.kill()
                process.wait()
                raise
            retcode = process.poll()
            if check and retcode:
                raise CalledProcessError(retcode, process.args,
                                         output=stdout, stderr=stderr)
        return CompletedProcess(process.args, retcode, stdout, stderr)
    print('V NOT > 3.5')
