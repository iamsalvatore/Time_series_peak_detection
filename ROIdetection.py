import pymzml

#Store values of peaks
class Peak(object):
    def __init__(self, mz, rt, i, scan):
        self.mz = mz
        self.rt = rt
        self.i = i
        self.scan = scan
        self.mean_mz = self.mz

    def __lt__(self,other):
        if self.mean_mz <= other.mean_mz:
            return True
        else:
            return False

    def __str__(self):
        return "({}, {}, {},)".format(self.mz, self.rt, self.i)

#Perform operation on a single ROI
class ROI(object):
    def __init__(self, peak):
        self.peak_list = []
        self.add_peak_to_roi(peak)

    def __str__(self):
        return "({})".format(self.mean_mz)
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

    def __lt__(self,other):
        if self.mean_mz <= other.mean_mz:
            return True
        else:
            return False
