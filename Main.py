import pymzml
import ROIdetection
import numpy as np


def get_ROIs(scan):
    # read all scans in mzML file
    rois = []
    for idx, mz in enumerate(scan.mz):
        peak = ROIdetection.Peak(mz, scan.scan_time[0], scan.i[idx], scan)
        roi = ROIdetection.ROI(peak)
        rois.append(roi)
    return rois


def main():
    rois = []
    dead_rois = []
    threshold = 2000
    run = pymzml.run.Reader(
        "/Users/salvatoreesposito/Downloads/Beer_multibeers_1_fullscan1.mzML")
    firstrun = True
    #for scan in list(run)[0:10]:
    for scan in run:
        if firstrun == True:
            print(scan.__dict__)
            rois = get_ROIs(scan)
            firstrun = False
            continue
        # mz can go into any ROI, but not mulitple roi
        extended_rois = []
        for idx, mz in enumerate(scan.mz):
            if scan.i[idx] < threshold:
                continue
            else:
                if rois == []:
                    peak = ROIdetection.Peak(
                        mz, scan.scan_time[0], scan.i[idx], scan)
                    roi = ROIdetection.ROI(peak)
                    extended_rois.append(roi)
                # here we create a new ROI
                else:
                    rois_mzs = [roi.mean_mz for roi in rois]
                    dist = abs(rois_mzs - mz)
                    closest_dist = np.array(dist).min()
                    if closest_dist < threshold:
                        closest_roi_index = np.argmin(np.array(dist))
                        peak = ROIdetection.Peak(
                            mz, scan.scan_time[0], scan.i[idx], scan)
                        rois[closest_roi_index].peak_list.append(peak)
                        extended_rois.append(rois[closest_roi_index])
                        rois.remove(rois[closest_roi_index])
                    # here we can add to an existing ROI
                    else:
                        peak = ROIdetection.Peak(
                            mz, scan.scan_time[0], scan.i[idx], scan)
                        roi = ROIdetection.ROI(peak)
                        extended_rois.append(roi)
                dead_rois = dead_rois + rois
                rois = extended_rois

    dead_rois = dead_rois + extended_rois

    completed_rois = []
    for saved_roi in dead_rois:
        peaklist = saved_roi.peak_list
        pmin = np.array([peak.i for peak in peaklist]).min()
        if pmin < threshold:
            completed_rois.append(saved_roi)

    for roi in completed_rois:
        print("ROI")
        for peak in roi.peak_list:
            print(peak)

    #     roi.save()

    # print(scan)
    # print(rois)


# if __name__ == "__main__":
main()

# rois = []
# dead_rois = []
# threshold = 0
# for scan in scans:
#     for mz in scan.mzs:
#         # mz can go into any ROI, but not mulitple roi
#         # multiple mz can go into one ROI (unlikely to happen very often)
#         if rois == []:
#             # here we create a new ROI
#         else:
#             roi_mzs = [roi.mean_mz for roi in rois]
#             dist = abs(rois_mzs - mz)
#             closest_dist = np.array(dist).min()
#             if closest_dist < threshold:
#                 # here we can add to an existing ROI
#             else:
#                 # here we create a new ROI
#     # here we want check whether an ROI has been extended
#     # if yes:
#         # keep in rois
#     # if no
#         # remove from rois, add to dead_rois
