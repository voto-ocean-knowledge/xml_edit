import subprocess
import logging
from add_all_nrt import proc_all_nrt
_log = logging.getLogger(__name__)


if __name__ == '__main__':
    logf = f'/data/log/all_nrt.log'
    logging.basicConfig(filename=logf,
                        filemode='a',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    _log.info("Start force add all nrt datasets to xml")
    proc_all_nrt(proc_all=True)
    subprocess.check_call(['/usr/bin/bash', "/home/usrerddap/erddap/xml_edit/correct_permissions.sh"])
    _log.info("Completed force add all nrt datasets to xml")
