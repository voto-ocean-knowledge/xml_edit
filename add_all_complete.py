import subprocess
import logging
import pathlib
import pandas as pd
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
    for glider, mission in glidermissions:
        mission_dir = f"/media/data/data_dir/complete_mission/SEA{glider}/M{mission}/timeseries"
        nc = list(pathlib.Path(mission_dir).glob("*.nc"))[0]
        size = nc.lstat().st_size
        gliders.append(glider)
        missions.append(mission)
        sizes.append(size/1e9)
        if size < 4e9:
            _log.info(f"Adding SEA{glider} M{mission}. Size {size/1e9} GB")
            subprocess.check_call(['/usr/bin/bash', "/home/ubuntu/xml_edit/add_dataset_complete.sh", str(glider), str(mission)])
            continue
        _log.info(f"SEA{glider} M{mission} is too large! {size/1e9} GB. Look for coarsened")
        coarse_dir = pathlib.Path(f"/media/data/data_dir/complete_mission/SEA{glider}/M{mission}/timeseries_1s")
        coarse_files = list(coarse_dir.glob("*.nc"))
        if coarse_files:
            nc_coarse = coarse_files[0]
            size = nc_coarse.lstat().st_size
            _log.info(f"Adding SEA{glider} M{mission} from 1s dir. Size {size / 1e9} GB")
            subprocess.check_call(['/usr/bin/bash', "/home/ubuntu/xml_edit/add_dataset_complete_1s.sh", str(glider), str(mission)])
        else:
            _log.warning(f"coarsened data in SEA{glider}/M{mission}/timeseries_1s not found. Skipping")
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
    _log.info("Completed add all complete datasets to xml")

