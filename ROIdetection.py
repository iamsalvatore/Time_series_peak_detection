import pymzml

#Store values of peaks
class Peak(object):
    def __init__(self, mz, rt, i, scan):
        self.mz = mz
        self.rt = rt
        self.i = i
        self.scan = scan

    def __str__(self):
        return "({}, {})".format(self.mz, self.rt)

#Perform operation on a single ROI
class ROI(object):
    def __init__(self, peak):
        self.peak_list = []
        self.add_peak_to_roi(peak)
#Update m/z mean
    def update_mean_mz(self):
        total = 0
        for peak in self.peak_list:
            total += peak.mz
        self.mean_mz = total / len(self.peak_list)

    def add_peak_to_roi(self, peak):
        self.peak_list.append(peak)
        self.update_mean_mz()

    def get_start_rt(self):
        return self.peak_list[0].rt  # assumes peaks are always in rt order

    def get_end_rt(self):
        return self.peak_list[-1].rt

    """ def processScans(self, path):
        run = pymzml.run.Reader(path)
        firstScan = run[0]
        firstScanRois = self.get_ROIs(firstScan)
        rois = []
        for scan in run[1:]:
            newRois = self.get_ROIs(scan)
            for roi in newRois:
                for firstroi in firstScanRois:
                    rois.append(roi)

        return rois

    def get_ROIs(self, scan):
        # read all scans in mzML file
        rois = []
        for peak in scan:
            p = peak(peak.mz, peak.rt, peak.intensity)
            roi = ROI(p)
            self.peak_list.append(peak)

        return rois """
