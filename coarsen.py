import xarray as xr
import pathlib
import logging
import pandas as pd
_log = logging.getLogger(__name__)


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
    ds.load()
    output_dir = pathlib.Path(f"/media/data/data_dir/complete_mission/SEA{glider}/M{mission}/timeseries_1s")
    if not pathlib.Path(output_dir).exists():
        pathlib.Path(output_dir).mkdir(parents=True)
    nc_name = nc.name
    output_nc = output_dir / nc_name
    ds.to_netcdf(output_nc)
    size = nc.lstat().st_size
    _log.info(f"SEA{glider} M{mission} post coarsen size {size/1e9} GB")
    

def coarsen_big():
    df_sizes = pd.read_csv("/media/data/log/sizes.csv")
    for row in df_sizes.iterrows():
        size = row.size_gb
        _log.info(f"SEA0{row.glider} M{row.mission} {size}GB")
        if size > 4:
            _log.info("start coarsen")
            coarsen(row.glider, row.mission)
    
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
    