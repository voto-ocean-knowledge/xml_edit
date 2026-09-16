import subprocess
import logging
from pathlib import Path
_log = logging.getLogger(__name__)


def proc_all_complete(proc_all=True):
    glider_paths = list(Path("/data/OG_complete").glob("*"))
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
        glidermission_xml = Path(f"/home/usrerddap/erddap/content/parts/OG_complete_{glider}_M{mission}.xml")
        if proc_all or not glidermission_xml.exists():
            _log.info(f"Add {glider} M{mission}")
            subprocess.check_call(['/usr/bin/bash', "/home/usrerddap/erddap/xml_edit/og_complete.sh", str(glider), str(mission)])
        else:
            _log.info(f"No update needed to {glider} M{mission}")


if __name__ == '__main__':
    logf = f'/data/log/og_complete.log'
    logging.basicConfig(filename=logf,
                        filemode='a',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    _log.info("Start add all complete datasets to xml")
    proc_all_complete()
    subprocess.check_call(['/usr/bin/bash', "/home/usrerddap/erddap/xml_edit/correct_permissions.sh"])
    _log.info("Completed add all complete datasets to xml")
