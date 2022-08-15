import xarray as xr
import numpy as np
import argparse
import pathlib
import logging
_log = logging.getLogger(__name__)


def chunk_ds(glider, mission):
    _log.info(f"start chunking SEA{glider} M{mission}")
    ds = xr.open_dataset(f"/media/data/data_dir/complete_mission/SEA{glider}/M{mission}/timeseries/mission_timeseries.nc")
    output_dir = pathlib.Path(f"/media/data/data_dir/complete_mission/SEA{glider}/M{mission}/timeseries_chunked")
    if not pathlib.Path(output_dir).exists():
        pathlib.Path(output_dir).mkdir(parents=True)
    length = len(ds.time)
    chunks = 10
    step_size = int(length/chunks)
    for i in range(chunks):
        start = i * step_size
        end = (i+1) * step_size
        if i + 1 == chunks:
            end = length
        _log.info(f"start {start} end {end}")
        ds_sub = ds.isel(time=np.arange(start, end))
        _log.info(f"{len(ds_sub.time)} {ds_sub.time.values[0]} {ds_sub.time.values[-1]}")
        ds_sub.to_netcdf(f"/media/data/data_dir/complete_mission/SEA{glider}/M{mission}/timeseries_chunked/mission_timeseries_{i}.nc")
    _log.info(f"Complete chunking SEA{glider} M{mission}")


if __name__ == '__main__':
    logf = f'/media/data/log/chunker.log'
    logging.basicConfig(filename=logf,
                        filemode='a',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    _log.info("Start add all complete datasets to xml")
    parser = argparse.ArgumentParser(description='process SX files with pyglider')
    parser.add_argument('glider', type=int, help='glider number, e.g. 70')
    parser.add_argument('mission', type=int, help='Mission number, e.g. 23')
    args = parser.parse_args()
    chunk_ds(args.glider, args.mission)
