import pymzml
import ROIdetection
import numpy as np
import bisect
import time
import CNN
import roi as nn_roi
import torch


def test_sorting():
    peaks = [ROIdetection.Peak(1, 2, 3, 4), ROIdetection.Peak(7, 2, 3, 4),
             ROIdetection.Peak(4, 2, 3, 4), ROIdetection.ROI(ROIdetection.Peak(5, 2, 3, 4))]
    peaks.sort()
    for peak in peaks:
        print(peak)


def create_roi_for_list(scan, idx, rois, scanidx):
    # creating peak object with mz, rt, intensity, scn
    peak = ROIdetection.Peak(
        scan.mz[idx], scan.scan_time[0], scan.i[idx], scanidx)
    # building a roi object with a peak we just constructed
    roi = ROIdetection.ROI(peak)
    # inserts roi into extended rois list
    bisect.insort(rois, roi)
    # here we create a new ROI
    return rois


def peakonly(num_of_scans=False,filepath = None):
    rois = []
    dead_rois = []
    intensity_threshold = 10000
    mzthreshold_min = 124
    mzthreshold_max = 127
    delta_mz = 0.005
    rt_min = 530
    rt_max = 600
    if filepath is None:
        filepath = "/Users/salvatoreesposito/Downloads/Beer_multibeers_1_fullscan1.mzML"
    run = pymzml.run.Reader(filepath)
    start = time.time()
    # print("Hello")
    for scanidx, scan in enumerate(run):
        if num_of_scans != False and scanidx == num_of_scans:
            break
        # print(scanidx)
        extended_rois = []
        if 500 < scan.scan_time[0] < 600:
            print(scan.scan_time[0])
            print(scan.scan_time[0] <= rt_max, scan.scan_time[0] >= rt_min)
        if scan.scan_time[0] <= rt_max and scan.scan_time[0] >= rt_min:
            print("Hello")
            # mz can go into any ROI, but not mulitple roi
            # loop over the mz values of a scan as well as the indexes
            for idx, mz in enumerate(scan.mz):
                if scan.i[idx] < intensity_threshold or mz >= mzthreshold_max or mz <= mzthreshold_min:
                    continue
                else:
                    if rois == []:
                        extended_rois = create_roi_for_list(
                            scan, idx, extended_rois, scanidx)
                    else:
                        # make a peak to find the insertion point
                        # of a real mz for comparison of
                        peak = ROIdetection.Peak(
                            mz, scan.scan_time[0], scan.i[idx], scanidx)
                        # if len(rois) != 1:
                        if len(rois) == 1:
                            closest_roi_index = 0
                        else:
                            high_index = bisect.bisect_left(rois, peak)
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
                        closest_dist = abs(rois[closest_roi_index].mean_mz - mz)
                        # check if the closest distance is less than the threshold
                        if closest_dist < delta_mz:
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
                                scan, idx, extended_rois, scanidx)
        dead_rois = dead_rois + rois
        rois = extended_rois
        print(len(rois),len(dead_rois),len(extended_rois))
    
    dead_rois = dead_rois + extended_rois
    print(len(dead_rois))
    # print(extended_rois)

# Check and cleanup
    completed_rois = []
    for saved_roi in dead_rois:
        peaklist = saved_roi.peak_list
        pmin = np.array([peak.mz for peak in peaklist]).min()
        # some rois have only 1 intesity 
        if len(peaklist) > 1:
            # if pmin < delta_mz:
            bisect.insort(completed_rois, saved_roi)

    end = time.time()
    print(end - start)
    print(len(completed_rois))

    # for roi in completed_rois:
    #     print(roi)
    #     # for peak in roi.peak_list:
    #     #     print(peak)
    # print(len(completed_rois))

    # classifier = CNN.load_model()
    # for roi in completed_rois:
    #     roi = nn_roi.ROI(scan=[roi.peak_list[0], roi.peak_list[-1]],
    #                      rt=[roi.peak_list[0].rt,
    #                          roi.peak_list[-1].rt],
    #                      i=[peak.i for peak in roi.peak_list],
    #                      mz=[peak.mz for peak in roi.peak_list],
    #                      mzmean=roi.mean_mz)
    #     if len(roi.i) != 1:
    #         print("ROI intensity: " + str(roi.mzmean), "CNN classifier: " +
    #               str(CNN.classifier_prediction(roi, classifier, torch.device("cpu"), points=256)))
    #     else:
    #         print("ROI intensity: " + str(roi.mzmean), "CNN classifier: " +
    #               str(CNN.classifier_prediction(roi, classifier, torch.device("cpu"), points=256)))

    return completed_rois
    
# # if __name__ == "__main__":
# peakonly(400)
