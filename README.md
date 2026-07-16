# ASL Translator and Emotion Communicator

A desktop application that translates American Sign Language (ASL) gestures and facial emotions in real-time using a webcam. This application is designed for people who are deaf or mute to help them communicate more effectively.

## Features

- Real-time hand gesture detection using MediaPipe Hands
- Custom gesture classification for ASL words using TensorFlow/Keras
- Facial emotion recognition using MediaPipe FaceMesh
- Completely offline functionality - no internet connection required
- Beautiful GUI with PyQt5 (Dark mode, Live camera feed, translation panel)
- Translation history saved locally
- Optional text-to-speech output (English and Hindi)

## Tech Stack

- Python 3.x
- OpenCV for webcam input
- MediaPipe (Hands, FaceMesh)
- TensorFlow/Keras or TFLite for gesture and emotion classification
- PyQt5 for user interface
- NumPy, Pandas for data processing

## Installation

1. Clone this repository
2. create a environment in this file (please note that I already created the enviroment .venv, if in case your system not accepting this delete .venv folder and create it)
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python main.py
```

## Incase the model doesn't supports your system
1. Note this mode require "Python 3.11", not currect version.
2. This model requries tensorflow, mediapipe, these requires "environment" i.e .venv
3. The model Requires 10 MB storage
4. Make sure you run the "run.py"
5. contact of me at my personal website ```https://vishal-r07.github.io/vishal-r/intro.html``` for any issues. 

## Data Folder:
Due to storage issue and not recuried for running this project I removed it. If incase developing the model or want to train it more words, here is the folder link:
```
https://drive.google.com/drive/folders/1mJXfKuhRFImjADvYirvfaifc9t4S53Bu?usp=drive_link
``` 
Note: Please make you allocate more than 2.7 GB storage to save it. These datas are completely reserved by Vishal Meyyappan R, Not for commercial use.
## Project Structure
Main files:
```
├── main.py                 # Main application entry point
├── requirements.txt        # Project dependencies
├── README.md              # Project documentation
├── assets/                # Images, icons, and other static assets
├── data/                  # Data for training models
├── models/                # Pre-trained models
│   ├── asl_model/         # ASL gesture recognition model
│   └── emotion_model/     # Facial emotion recognition model
└── src/                   # Source code
    ├── gui/               # PyQt5 GUI components
    ├── asl/               # ASL detection and classification
    ├── emotion/           # Emotion detection and classification
    ├── utils/             # Utility functions
    └── history/           # Translation history management
```

## Team VYARK

1. Vishal Meyyappan R - @vishal-r07 - ML creation and lead programmer
2. Kishore V S - @Kishore-vs - UI designer and lead programmer
3. Ashwin R - @ashwinr-act-cit - Dataset management and ML creation
4. Rayhan Hameed - @Ray-5106 - Dataset management and GUI supervisor
5. Yuvan Shankar - lead programmer and ML trainner

## License

All rights reserved by VYARK team
