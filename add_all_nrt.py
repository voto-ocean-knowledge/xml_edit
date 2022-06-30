import subprocess
from correct_xml import update_doc
import logging
import pathlib
_log = logging.getLogger(__name__)


def proc_all_nrt():
    glider_paths = list(pathlib.Path("/media/data/data_dir//nrt").glob("SEA*"))
    glidermissions = []
    for glider_path in glider_paths:
        mission_paths = glider_path.glob("M*")
        for mission_path in mission_paths:
            try:
                glidermissions.append((int(glider_path.parts[-1][3:]), int(mission_path.parts[-1][1:])))
            except:
                _log.warning(f"Could not process {mission_path}")
    for glider, mission in glidermissions:
        _log.info(f"Adding SEA{glider} M{mission}")
        subprocess.check_call(['/usr/bin/bash', "/home/ubuntu/xml_edit/add_dataset_nrt.sh", glider, mission])
        update_doc(glider, mission, "nrt")


if __name__ == '__main__':
    logf = f'/media/data/log/all_nrt.log'
    logging.basicConfig(filename=logf,
                        filemode='w',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    _log.info("Start add all nrt datasets to xml")
    proc_all_nrt()
    _log.info("Completed add all nrt datasets to xml")

