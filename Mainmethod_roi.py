import pymzml
import ROIdetection


def get_ROIs(scan):
    # read all scans in mzML file
    rois = []
    for i in range(len(scan.mz)):
        p = ROIdetection.Peak(scan.mz[i], scan.scan_time[0], scan.mz[i], scan.i)
        roi = ROIdetection.ROI(p)
        rois.append(roi)

    return rois


"""
scan1ROIS = [ROI1,ROI2,...ROIN]

newROIS = []
loop over scan 2 -> N:
    for s1Roi in scan1ROIS:
        for mz in scan:
            if mz ~ s1Roi.mzmean():
                p = Peak(mz,...)
                s1Roi.add_peak(p)
            else:
                p = Peak(mz,...)
                roi = ROI(p)
                newROIS.append(roi) """

# if newROIS not needed, append to scan1ROIS


def main():
    threshold = 2
    run = pymzml.run.Reader(
        "/Users/salvatoreesposito/Downloads/Beer_multibeers_1_fullscan1.mzML")
    firstScan = run[1]
    firstScanRois = get_ROIs(firstScan)
    firstrun=True
    for scan in run:
        print("hello")
        if firstrun==True:
            firstrun=False
            continue
        for roi in firstScanRois:
            for j in range (len(scan.mz)):
                if scan.mz[j] > (roi.mean_mz - threshold) and scan.mz[j]< (roi.mean_mz+threshold):
                    newpeak = ROIdetection.Peak( # loop over the mz
                        scan.mz[j], scan.scan_time[0], scan.mz[j], scan.i)
                    roi.add_peak_to_roi(newpeak)
                    break
                else:
                    newpeak = ROIdetection.Peak(
                        scan.mz[j], scan.scan_time[0], scan.mz[j], scan.i)
                    newroi = ROIdetection.ROI(newpeak)
                    firstScanRois.append(newroi)
                    break
        
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
#         # keep in roi
#     # if no
#         # remove from roi, add to dead_rois