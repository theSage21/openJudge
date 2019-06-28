import requests
import logging
import subprocess
import os

logger = logging.getLogger(__name__)


def run(endpoint, workdir):
    while True:
        try:
            job = requests.get(endpoint + "/runnerjob").json()
            checkid = job["checkid"]
            cmd, inp, code, fname = job["cmd"], job["inp"], job["code"], job["fname"]
            root = workdir / checkid
            os.mkdir(root)
            with open(root / fname, "w") as fl:
                fl.write(code)
            with open(root / "inp", "w") as fl:
                fl.write(inp)
            cmd = cmd.format(fpath=fpath, inp=root / "inp")
            proc = subprocess.run([cmd], shell=True, capture_output=True)
            requests.post(
                endpoint + "/runnerjob",
                json={
                    "checkid": checkid,
                    "stdout": proc.stdout.decode(),
                    "stderr": proc.stderr.decode(),
                    "exit_code": proc.returncode,
                },
            )
        except Exception as e:
            logger.exception(e)
