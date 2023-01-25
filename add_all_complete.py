import subprocess
import logging
import pathlib
import pandas as pd
from chunker import chunk_ds
from times_track import update_proc_time, update_erddap_time, erddap_needs_update
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
    gliders, missions, sizes = [], [], []
    total = len(glidermissions)
    for i , (glider, mission) in enumerate(glidermissions):
        mission_dir = f"/media/data/data_dir/complete_mission/SEA{glider}/M{mission}/timeseries"
        _log.info(f"{i}/{total}: Check SEA{glider} M{mission}")
        update_proc_time(glider, mission, "complete")
        if not erddap_needs_update(glider, mission, "complete"):
            continue
        nc = list(pathlib.Path(mission_dir).glob("*.nc"))[0]
        size = nc.lstat().st_size
        gliders.append(glider)
        missions.append(mission)
        sizes.append(size/1e9)
        if size < 4e9:
            _log.info(f"Adding SEA{glider} M{mission}. Size {size/1e9} GB")
            subprocess.check_call(['/usr/bin/bash', "/home/ubuntu/xml_edit/add_dataset_complete.sh", str(glider), str(mission)])
            update_erddap_time(glider, mission, "complete")
            continue
        _log.info(f"SEA{glider} M{mission} is too large! {size/1e9} GB. Look for chunked")
        chunk_ds(glider, mission)
        _log.info(f"Adding SEA{glider} M{mission} from coarse dir")
        subprocess.check_call(['/usr/bin/bash', "/home/ubuntu/xml_edit/add_dataset_chunked.sh", str(glider), str(mission)])
        update_erddap_time(glider, mission, "complete")
    df_sizes = pd.DataFrame({"glider": gliders, "mission": missions, "size_gb": sizes})
    df_sizes.to_csv("/media/data/log/sizes.csv", index=False)


if __name__ == '__main__':
    logf = f'/media/data/log/all_complete.log'
    logging.basicConfig(filename=logf,
                        filemode='a',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    _log.info("Start add all complete datasets to xml")
    proc_all_nrt()
    subprocess.check_call(['/usr/bin/bash', "/home/ubuntu/xml_edit/correct_permissions.sh"])
    _log.info("Completed add all complete datasets to xml")

