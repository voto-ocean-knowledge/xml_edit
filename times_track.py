import datetime
import pandas as pd
import numpy as np
import pathlib
import logging
_log = logging.getLogger(__name__)


def update_proc_time(glider, mission, file_type):
    if file_type == "complete":
        path_base = pathlib.Path(f"/media/data/data_dir/complete_mission/SEA{glider}/M{mission}/timeseries")
    else:
        path_base = pathlib.Path(f"/media/data/data_dir/nrt/SEA{glider}/M{mission}/timeseries")
    path = list(path_base.glob("*.nc"))[0]
    mtime = datetime.datetime.fromtimestamp(path.lstat().st_mtime)
    fn = f"/media/data/log/{file_type}.csv"
    df = pd.read_csv(fn, parse_dates=["proc_time", "erddap_time"])
    a = [np.logical_and(df.glider == glider, df.mission == mission)]
    if df.index[tuple(a)].any():
        ind = df.index[tuple(a)].values[0]
        df.at[ind, "proc_time"] = mtime
    else:
        new_row = pd.DataFrame({"glider": glider, "mission": mission,
                                "proc_time": mtime, "erddap_time": datetime.datetime(1970, 1, 1)}, index=[len(df)])
        df = pd.concat((df, new_row))
    df.sort_values("proc_time", inplace=True)
    _log.info(f"updated processing time to {mtime}")
    df.to_csv(fn, index=False)


def update_erddap_time(glider, mission, file_type):
    fn = f"/media/data/log/{file_type}.csv"
    df = pd.read_csv(fn, parse_dates=["proc_time", "erddap_time"])
    a = [np.logical_and(df.glider == glider, df.mission == mission)]
    if df.index[tuple(a)].any():
        ind = df.index[tuple(a)].values[0]
        df.at[ind, "erddap_time"] = datetime.datetime.now()
    else:
        new_row = pd.DataFrame({"glider": glider, "mission": mission,
                                "erddap_time": datetime.datetime.now()}, index=[len(df)])
        df = pd.concat((df, new_row))
    df.sort_values("proc_time", inplace=True)
    _log.info(f"updated erddap time to {datetime.datetime.now()}")
    df.to_csv(fn, index=False)


def erddap_needs_update(glider, mission, file_type):
    fn = f"/media/data/log/{file_type}.csv"
    df = pd.read_csv(fn, parse_dates=["proc_time", "erddap_time"])
    a = [np.logical_and(df.glider == glider, df.mission == mission)]
    if df.index[tuple(a)].any():
        ind = df.index[tuple(a)].values[0]
        row = df.loc[ind]
        if row.proc_time > row.erddap_time:
            return True
    return False
