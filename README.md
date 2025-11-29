
# Multiple Object Tracking with Motion Detection and Kalman Filters

This project implements multiple object detection and tracking using motion-based detection and Kalman filters. It includes a PySide6-based graphical interface for loading videos, stepping through frames, and visualizing tracked objects over time.

The application processes a video file frame-by-frame, detects moving objects using three-frame differencing, and assigns each object to an individual Kalman filter for prediction and smoothing. Trails of past positions are drawn directly onto the video frames for visualization.

---

## File Structure

```
kalman_filter.py       # Kalman filter implementation
motion_detection.py    # Motion detection using 3-frame differencing and morphology
tracking.py            # Full GUI application and multi-object tracker
qtdemo.py              # Example PySide6 demo (optional reference)
environment.yml        # Conda environment setup
```

---

## Installation

You can install all dependencies using the provided `environment.yml`:

```bash
conda env create -f environment.yml
conda activate tracking
```

Alternatively, install dependencies manually:

```bash
pip install numpy opencv-python scikit-image PySide6
```

---

## System Overview

### 1. Motion Detection  
Implemented in `motion_detection.py`.

The system detects motion using three consecutive frames:

- f1 = frame[t-2]
- f2 = frame[t-1]
- f3 = frame[t]

The detection process:

1. Compute absolute differences between frames  
2. Take the minimum difference to reduce noise  
3. Apply a threshold  
4. Apply morphological closing and dilation  
5. Label connected components  
6. Return bounding boxes for sufficiently large regions  

The result is a set of motion-based object proposals for each frame.

---

### 2. Kalman Filtering  
Implemented in `kalman_filter.py`.

Each tracked object uses a Kalman filter with a four-dimensional state vector:

```
[x, y, vx, vy]^T
```

Functions:

- `predict()` estimates the next position  
- `update()` incorporates new measurements  
- Position history is stored for visualization  

---

### 3. Multi-Object Tracking  
Implemented inside `tracking.py`.

Features:

- Matches detected bounding boxes to existing filters using distance thresholding  
- Creates new filters for unseen objects  
- Removes objects that have not received measurements for several frames  
- Supports tracking multiple objects simultaneously  

---

### 4. Graphical User Interface  
Implemented in `tracking.py`.

Capabilities:

- Load a video file (.mp4 or .avi)
- Step through frames one at a time
- Jump forward or backward by 60 frames
- Reset the tracker at any frame
- Reprocess tracking automatically when navigating backward
- Render current predicted position and all historical points

Run the GUI with:

```bash
python tracking.py
```

---

## How to Run

1. Navigate to the directory containing the project files  
2. Activate the environment  
3. Run the application:

```bash
python tracking.py
```

4. Use the interface:

| Button | Description |
|--------|-------------|
| Load Video | Select a video file |
| < Back | Step back 1 frame |
| Next Frame | Step forward 1 frame |
| << Back 60 | Jump backward 60 frames |
| Forward 60 >> | Jump forward 60 frames |
| Reset | Reset tracker at current frame |

Objects will be detected and tracked automatically as frames advance.

---

## Notes

- The first three frames are required before motion detection begins.
- Tracker state resets when jumping backward to maintain consistency.
- Performance depends on video resolution and motion complexity.

---

## License

This project is provided for educational and demonstration purposes.
