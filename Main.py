import pymzml
import ROIdetection
import numpy as np
import bisect
import time
import CNN


def test_sorting():
    peaks = [ROIdetection.Peak(1, 2, 3, 4), ROIdetection.Peak(7, 2, 3, 4), ROIdetection.Peak(
        4, 2, 3, 4), ROIdetection.ROI(ROIdetection.Peak(5, 2, 3, 4))]
    peaks.sort()
    for peak in peaks:
        print(peak)


def create_roi_for_list(scan, idx, rois):
    # creating peak object with mz, rt, intensity, scn
    peak = ROIdetection.Peak(
        scan.mz[idx], scan.scan_time[0], scan.i[idx], scan)
    # building a roi object with a peak we just constructed
    roi = ROIdetection.ROI(peak)
    # inserts roi into extended rois list
    bisect.insort(rois, roi)
    # here we create a new ROI
    return rois


def main():
    rois = []
    dead_rois = []
    threshold = 1000000
    mzthreshold = 0.005
    run = pymzml.run.Reader(
        "/Users/salvatoreesposito/Downloads/Beer_multibeers_1_fullscan1.mzML")
    start = time.time()
    # for scan in list(run)[0:5]:
    for scan in run:
        # mz can go into any ROI, but not mulitple roi
        extended_rois = []
        print(len(extended_rois))
        # loop over the mz values of a scan as well as the indexes
        for idx, mz in enumerate(scan.mz):
            if scan.i[idx] < threshold:
                continue
            else:
                if rois == []:
                    extended_rois = create_roi_for_list(
                        scan, idx, extended_rois)
                else:
                    # make a peak to find the insertion point of a real mz for comparison of
                    peak = ROIdetection.Peak(
                        mz, scan.scan_time[0], scan.i[idx], scan)
                    # if len(rois) != 1:
                    if len(rois) == 1:
                        closest_roi_index = 0
                    else:
                        high_index = bisect.bisect_right(rois, peak)
                        low_index = high_index-1
                        if high_index == len(rois):
                            closest_roi_index = low_index
                        else:
                            dist_high = abs(rois[high_index].mean_mz - mz)
                            dist_low = abs(rois[low_index].mean_mz - mz)
                            if dist_low < dist_high:
                                closest_roi_index = low_index
                            else:
                                closest_roi_index = high_index
                    # use the index to find the closest roi in the rois list
                    # and get the mean mz from it
                    closest_dist = rois[closest_roi_index].mean_mz
                    # check if the closest distance is less than the threshold
                    if closest_dist < mzthreshold:
                        # and use the index to find the roi in the rois list
                        # and append
                        closest_roi = rois[closest_roi_index]
                        closest_roi.add_peak_to_roi(peak)
                        # inserting the closest roi into the extended rois list
                        bisect.insort(extended_rois, closest_roi)
                        del rois[closest_roi_index]
                    # here we can add to an existing ROI
                    else:
                        extended_rois = create_roi_for_list(
                            scan, idx, extended_rois)
                dead_rois = dead_rois + rois
                rois = extended_rois
    dead_rois = dead_rois + extended_rois
    # print(extended_rois)

    completed_rois = []
    for saved_roi in dead_rois:
        peaklist = saved_roi.peak_list
        pmin = np.array([peak.mz for peak in peaklist]).min()
        if pmin < threshold:
            bisect.insort(completed_rois, saved_roi)

    end = time.time()
    print(end - start)

    for roi in completed_rois:
        print(roi)
        # for peak in roi.peak_list:
        #     print(peak)
    print(len(completed_rois))

    classifier = CNN.load_model()
    for roi in completed_rois:
        roi = roi.ROI(roi.scan, )
        CNN.classifier_prediction(roi, classifier, cpu, points=256)


# if __name__ == "__main__":
main()
