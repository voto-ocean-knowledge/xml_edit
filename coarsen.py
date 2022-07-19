import xarray as xr
import pathlib
import logging
import pandas as pd
from datetime import datetime, timezone
_log = logging.getLogger(__name__)


def simple_timestamp(mtime):
    modified = datetime.fromtimestamp(mtime, tz=timezone.utc)
    return str(modified)[:16]


def coarsen(glider, mission):
    input_dir = f"/media/data/data_dir/complete_mission/SEA{glider}/M{mission}/timeseries"
    nc = list(pathlib.Path(input_dir).glob("*.nc"))[0]
    ds = xr.open_dataset(nc)
    ds = ds.drop_duplicates(dim="time")
    ds["depth2"] = ds.depth
    ds["longitude2"] = ds.longitude
    ds["latitude2"] = ds.latitude
    ds = ds.resample(time="1S").nearest()
    ds = ds.assign_coords(coords={"depth": ds.depth2})
    ds = ds.assign_coords(coords={"longitude": ds.longitude2})
    ds = ds.assign_coords(coords={"latitude": ds.latitude2})
    ds = ds.drop_vars(["depth2", "latitude2", "longitude2"])
    output_dir = pathlib.Path(f"/media/data/data_dir/complete_mission/SEA{glider}/M{mission}/timeseries_1s")
    if not pathlib.Path(output_dir).exists():
        pathlib.Path(output_dir).mkdir(parents=True)
    nc_name = nc.name
    output_nc = output_dir / nc_name
    ds.load()
    ds.to_netcdf(output_nc)
    size = output_nc.lstat().st_size
    _log.info(f"SEA{glider} M{mission} post coarsen size {size/1e9} GB")
    

def coarsen_big():
    df_sizes = pd.read_csv("/media/data/log/sizes.csv")
    for i, row in df_sizes.iterrows():
        glider = int(row.glider)
        mission = int(row.mission)
        size = row.size_gb
        _log.info(f"SEA0{glider} M{mission} {size}GB")
        if size < 4:
            continue
        output_dir = pathlib.Path(f"/media/data/data_dir/complete_mission/SEA{glider}/M{mission}/timeseries_1s")
        og_nc = list(pathlib.Path(f"/media/data/data_dir/complete_mission/SEA{glider}/M{mission}/timeseries").glob("*.nc"))[0]
        if output_dir.exists:
            nc_list = list(output_dir.glob("*.nc"))
            if nc_list:
                nc = nc_list[0]
                _log.info(f"Original nc modified at {simple_timestamp(og_nc.lstat().st_atime)}")
                _log.info(f"Coarse nc modified at {simple_timestamp(nc.lstat().st_atime)}")
                if og_nc.lstat().st_atime > nc.lstat().st_atime:
                    _log.info("No change to original nc since last coarsen. Skipping")
                    continue
        _log.info("start coarsen")
        coarsen(glider, mission)


if __name__ == '__main__':
    logf = f'/media/data/log/coarsen.log'
    logging.basicConfig(filename=logf,
                        filemode='a',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    _log.info("Start dataset coarsening")
    coarsen_big()
    _log.info("Completed coarsening")
