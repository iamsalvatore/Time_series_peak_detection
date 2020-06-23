
import pymzml
import numpy as np
import pandas as pd


def get_ROIs(path,  delta_mz=0.005,  required_points=15,  dropped_points=3, progress_callback=None):
    # read all scans in mzML file
    run = pymzml.run.Reader(path)
    scans = pd.DataFrame()
    for scan in run:
        if scan.ms_level == 1:
            s = pd.Series(index=["index", "mz", "scantime"],
                          data=[scan.i, scan.mz, scan.scan_time[0]])
            s = pd.DataFrame(s).T
            scans = scans.append(pd.DataFrame(s))
    scans = scans.reset_index(drop=True)
    print(np.mean(scans["mz"].iloc[0]))

    rois = pd.DataFrame()
    process_rois = pd.DataFrame()

    init_scan = scans.iloc[0]
    start_time = init_scan["scantime"]  # retention time
    min_mz = min(init_scan["mz"])
    max_mz = max(init_scan["mz"])
    for n in range(len(init_scan["index"])):
        if init_scan["index"][n] != 0:
            new_roi = pd.Series(index=["scan_begin", "scan_end", "rt_begin", "rt_end", "i", "mz", "mz_mean", "points"],
                                data=[0, 0, start_time, start_time, init_scan["index"][n], init_scan["mz"][n], init_scan["mz"][n], 1])
            new_roi = pd.DataFrame(new_roi).T
          #  process_rois[init_scan.mz[n]] = new_roi
            process_rois = process_rois.append(new_roi)

    process_rois = process_rois.reset_index(drop=True)
    print(process_rois)
    process_rois.to_csv("ROIscans")


print(get_ROIs("/Users/salvatoreesposito/Downloads/Beer_multibeers_1_fullscan1.mzML"))
