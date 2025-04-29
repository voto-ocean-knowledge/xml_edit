import subprocess
import logging
import pathlib
from times_track import update_proc_time, update_erddap_time, erddap_needs_update
_log = logging.getLogger(__name__)


def proc_all_nrt(proc_all=False):
    glider_paths = list(pathlib.Path("/data/nrt").glob("*"))
    glidermissions = []
    for glider_path in glider_paths:
        mission_paths = glider_path.glob("M*")
        for mission_path in mission_paths:
            try:
                glidermissions.append((glider_path.parts[-1], int(mission_path.parts[-1][1:])))
            except:
                _log.warning(f"Could not process {mission_path}")

    _log.info(f"found {len(glidermissions)} glider missions to add")
    for glider, mission in glidermissions:
        update_proc_time(glider, mission, "nrt")
        if erddap_needs_update(glider, mission, "nrt") or proc_all:
            _log.info(f"Add {glider} M{mission}")
            subprocess.check_call(['/usr/bin/bash', "/home/usrerddap/erddap/xml_edit/add_dataset_nrt.sh", str(glider), str(mission)])
            update_erddap_time(glider, mission, "nrt")
        else:
            _log.info(f"No update needed to {glider} M{mission}")


if __name__ == '__main__':
    logf = f'/data/log/all_nrt.log'
    logging.basicConfig(filename=logf,
                        filemode='a',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    _log.info("Start add all nrt datasets to xml")
    proc_all_nrt()
    subprocess.check_call(['/usr/bin/bash', "/home/usrerddap/erddap/xml_edit/correct_permissions.sh"])
    _log.info("Completed add all nrt datasets to xml")

