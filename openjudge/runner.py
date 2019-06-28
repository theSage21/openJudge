import requests
import logging
import subprocess
import os

logger = logging.getLogger(__name__)


def run(endpoint, workdir):
    while True:
        try:
            job = requests.get(endpoint + "/runnerjob")
            print(job.status_code)
            print(job.text)
            job = job.json()
            checkid = job["checkid"]
            root = workdir / checkid
            os.mkdir(root)
            fpath, inpath = root / job["fname"], root / "input"
            with open(fpath, "w") as fl:
                fl.write(job["code"])
            with open(inpath, "w") as fl:
                fl.write(job["inp"])
            cmd = cmd.format(fpath=fpath, inp=inpath)
            try:
                proc = subprocess.run(
                    [cmd], shell=True, capture_output=True, timeout=job["timeout"]
                )
                is_timeout = False
            except subprocess.TimeoutExpired:
                is_timeout = True
            requests.post(
                endpoint + "/runnerjob",
                json={
                    "checkid": checkid,
                    "stdout": proc.stdout.decode(),
                    "stderr": proc.stderr.decode(),
                    "exit_code": proc.returncode,
                    "is_timeout": is_timeout,
                },
            )
        except Exception as e:
            logger.exception(e)
