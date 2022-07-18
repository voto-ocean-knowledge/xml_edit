import subprocess
import logging
import pathlib
_log = logging.getLogger(__name__)


def proc_all_nrt():
    glider_paths = list(pathlib.Path("/media/data/data_dir/complete_mission").glob("SEA*"))
    glidermissions = []
    for glider_path in glider_paths:
        mission_paths = glider_path.glob("M*")
        for mission_path in mission_paths:
            try:
                glidermissions.append((int(glider_path.parts[-1][3:]), int(mission_path.parts[-1][1:])))
            except:
                _log.warning(f"Could not process {mission_path}")

    _log.info(f"found {len(glidermissions)} glider missions to add")
    for glider, mission in glidermissions:
        mission_dir = f"/media/data/data_dir/complete_mission/SEA{glider}/M{mission}/timeseries"
        nc = list(pathlib.Path(mission_dir).glob("*.nc"))[0]
        size = nc.lstat().st_size
        if size > 3e9:
            _log.warning(f"SEA{glider} M{mission} is too large! {size/1e9} GB. Skipping")
            continue
        _log.info(f"Adding SEA{glider} M{mission}. Size {size/1e9} GB")
        subprocess.check_call(['/usr/bin/bash', "/home/ubuntu/xml_edit/add_dataset_complete.sh", str(glider), str(mission)])


if __name__ == '__main__':
    logf = f'/media/data/log/all_complete.log'
    logging.basicConfig(filename=logf,
                        filemode='a',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    _log.info("Start add all complete datasets to xml")
    proc_all_nrt()
    _log.info("Completed add all complete datasets to xml")

