import pymzml
import ROIdetection
import numpy as np
import bisect
import time
import CNN
import roi as nn_roi
import torch



def create_roi_for_list(scan, idx, rois, scanidx):
    """
    Creates a peak objects and builds an ROI with a peak

    """
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
    intensity_threshold = 1000
    mzthreshold_min = 116
    mzthreshold_max = 116.3
    delta_mz = 0.005
    rt_min = 440
    rt_max = 550
    # sys.maxsize
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
        # if 500 < scan.scan_time[0] < 600:
        #     print(scan.scan_time[0])
        #     print(scan.scan_time[0] <= rt_max, scan.scan_time[0] >= rt_min)
        if scan.scan_time[0] <= rt_max and scan.scan_time[0] >= rt_min:
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
        # print(len(rois),len(dead_rois),len(extended_rois))
    
    dead_rois = dead_rois + extended_rois
    # print(len(dead_rois))
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
    # print(end - start)
    # print(len(completed_rois))

    return completed_rois


def sub_rois (roi, percentage=10):
    multiple_rois=[]
    length_difference =  roi.get_end_rt()-roi.get_start_rt()
    num_seconds = length_difference*(percentage/100)
    total_seconds=num_seconds
    # split the rois while the max rt is still less than the total num of seconds
    for i in  range(int(100/percentage)+1):
        # make an array of rt where the rt is less then the min rt plus the num of seconds
        retention_times = [peak.rt for peak in roi.peak_list if peak.rt < roi.get_start_rt()+total_seconds]
        # get the mzs correlated with the retention times
        mz = [peak.mz for peak in roi.peak_list[:len(retention_times)]]
        # get the intensities correlated with the retention times
        intensity = [peak.i for peak in roi.peak_list[:len(retention_times)]]
        scan_number = [peak.scan for peak in roi.peak_list[:len(retention_times)]]
        mean_mz = np.mean(mz)
        peaks = []
        # list of peaks for the roi
        for i in range(len(retention_times)):
            peaks.append(ROIdetection.Peak(mz[i], retention_times[i], intensity[i], scan_number[i]))
        # adding peaks to the roi
        new_roi = 0
        for idx, peak in enumerate (peaks):
            if idx == 0:
                new_roi = ROIdetection.ROI(peak)
            new_roi.add_peak_to_roi(peak)
        multiple_rois.append(new_roi)
        # increase num of seconds until over the maximum
        total_seconds += num_seconds
    return multiple_rois