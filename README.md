
# Mass Spectrometry Peak Detection Project

## Overview
This project focuses on the detection of peaks in mass spectrometry data using Python. It involves the use of `pymzml` for processing mzML files, a common format in mass spectrometry data analysis. The project comprises two main scripts: `roi_detection.py` and `main.py`.

### `roi_detection.py`
- Defines classes `Peak` and `ROI` (Region of Interest) for managing mass spectrometry data.
- `Peak`: Represents a single peak in the mass spectrometry data.
- `ROI`: Handles operations on a single Region of Interest.

### `main.py`
- Utilizes `roi_detection.py` for peak detection and ROI management.
- Integrates with other modules like `numpy`, `torch`, and custom modules (`CNN`, `roi`) for further data processing and neural network operations.

## Installation and Dependencies
- Python (version specified in `requirements.txt`)
- Dependencies: `pymzml`, `numpy`, `torch`, and other modules as required by the project.
  ```
  pip install -r requirements.txt
  ```

## Usage
- Process mzML files using `pymzml` within the provided scripts.
- `roi_detection.py` can be used to detect peaks and manage ROIs in the data.
- `main.py` serves as the entry point for the application, leveraging the functionality provided by `roi_detection.py` and integrating additional processing and neural network operations.

## Contributing
Contributions to enhance and expand the functionality of this peak detection project are welcome. Please adhere to standard coding practices and provide documentation for any new features or improvements.

## License
University of Glasgow 2020