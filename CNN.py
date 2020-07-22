import torch
import numpy as np
from scipy.interpolate import interp1d

def load_model():
    # Model class must be defined somewhere
    model = torch.load(
        "/Users/salvatoreesposito/Downloads/peakonly-master/data/weights")
    model.eval()
    return model


def preprocess(signal, device, interpolate=False, length=None):
    """
    :param signal: intensities in roi
    :param device: cpu or gpu
    :param points: number of point needed for CNN
    :return: preprocessed intensities which can be used in CNN
    """
    if interpolate:
        interpolate = interp1d(np.arange(len(signal)), signal, kind='linear')
        signal = interpolate(np.arange(length) /
                             (length - 1) * (len(signal) - 1))
    signal = torch.tensor(signal / np.max(signal),
                          dtype=torch.float32, device=device)
    return signal.view(1, 1, -1)


def classifier_prediction(roi, classifier, cpu, points=256):
    """
    :param roi: an ROI object
    :param classifier: CNN for classification
    :param device: cpu or gpu
    :param points: number of point needed for CNN
    :return: class/label
    """
    signal = preprocess(roi.i, cpu, points)
    proba = classifier(signal)[0].softmax(0)
    return np.argmax(proba.cpu().detach().numpy())
