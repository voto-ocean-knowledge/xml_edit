import xarray as xr
import pandas as pd
from pathlib import Path
import glob

dataset_dir = Path("/data/meta")


def update_file_dates(dataset_nc):
    ds = xr.open_dataset(dataset_nc)
    try:
        df = pd.read_csv(dataset_dir / "dataset_times.csv", index_col=0)
    except:
        df = pd.DataFrame()
    ds_id = ds.attrs['dataset_id']
    nc_time = ds.attrs["date_created"]
    new_stats = {"date_created": pd.to_datetime(nc_time)}
    if ds_id in df.index:
        df.loc[ds_id] = new_stats
    else:
        new_row = pd.DataFrame(new_stats, index=[ds_id])
        df = pd.concat((df, new_row))
    df = df.sort_index()
    df.to_csv(dataset_dir / "dataset_times.csv")
    ds.close()


if __name__ == '__main__':
    infiles = glob.glob("/data/complete_mission/*/M*/timeseries/mission_timeseries*.nc")

    for infile in infiles:
        update_file_dates(infiles)