import pymzml
import ROIdetection
import numpy as np


def get_ROIs(scan):
    # read all scans in mzML file
    rois = []
    for i in range(len(scan.mz)):
        p = ROIdetection.Peak(
            scan.mz[i], scan.scan_time[0], scan.mz[i], scan.i)
        roi = ROIdetection.ROI(p)
        rois.append(roi)
    return rois


def main():
    rois = []
    dead_rois = []
    threshold = 2
    run = pymzml.run.Reader(
        "/Users/salvatoreesposito/Downloads/Beer_multibeers_1_fullscan1.mzML")
    firstrun = True
    for scan in run:
        if firstrun == True:
            firstScanRois = get_ROIs(scan)
            firstrun = False
            continue
        # mz can go into any ROI, but not mulitple roi
        # multiple mz can go into one ROI (unlikely to happen very often)
        extended_roi_indexes = []
        for mz in scan.mz:
            if rois == []:
                peak = ROIdetection.Peak(mz)
                roi = ROIdetection.ROI(peak)
                rois.append(roi)
            # here we create a new ROI
            else:
                rois_mzs = [roi.mean_mz for roi in rois]
                dist = abs(rois_mzs - mz)
                closest_dist = np.array(dist).min()
                if closest_dist < threshold:
                    closest_roi_index = np.argmin(np.array(dist))
                    peak = ROIdetection.Peak(mz)
                    rois[closest_roi_index].peak_list.append(peak)
                    extended_roi_indexes.append(closest_roi_index)
                # here we can add to an existing ROI
                else:
                    peak = ROIdetection.Peak(mz)
                    roi = ROIdetection.ROI(peak)
        temp_rois = []
        temp_dead_rois = []
        for i in range(len(rois)):
            if i in extended_roi_indexes:
                temp_rois.append(rois[i])
            else:
                temp_dead_rois.append(rois[i])
        rois = temp_rois
        dead_rois = temp_dead_rois

    for roi in rois:
        roi.save()

    print(scan)
    print(firstScanRois)


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
