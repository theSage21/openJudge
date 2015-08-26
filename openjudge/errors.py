class OpenjudgeError(Exception):
    "Base class for openjudge exceptions"
    pass


class InterfaceNotRunning(OpenjudgeError):
    pass


class Timeout(OpenjudgeError):
    pass


class SlaveShutdown(OpenjudgeError):
    pass
