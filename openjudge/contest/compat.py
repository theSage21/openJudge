import sys

if sys.version_info >= (3, 5):
    from subprocess import (run,
                            PIPE,
                            TimeoutExpired)
    print('V> 3.5')

else:

    from contest.sub35 import (PIPE,
                               Popen,
                               TimeoutExpired,
                               CalledProcessError,
                               CompletedProcess,
                               run)
    print('V NOT > 3.5')
