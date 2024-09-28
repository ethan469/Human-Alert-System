# Human-Alert-System
This Python 3 computer vision project is intended to run on the Jetson Nano. The project processes image data from a configured video input such as a USB web camera, processes the image with object detection networks, and outputs a message to the console when a person is detected in the video stream. The long-term goals or this project are to save an image or video clip when a person is detected and send it to the user via email.


# Setting up the project:
1. Setup the prerequisite jetson-inference project by following their instruction at (https://github.com/dusty-nv/jetson-inference/).
2. Clone this repository
3. Run the Python 3 script "Detection.py" to run the program

# Program Arguments
* input_URI - this argument determines which camera is used for the input video stream; defaults to "/dev/video0".
* output_URI - this argument determines what output is saved from the video stream; defaults to "output.mp4"
* overlay - this argument adds bounding boxes and labels the detected objects in the video stream; defaults to "box,labels,conf" for box, and confidence
* threshold - this argument controls the minimum confidence threshold to label an object in the stream; defaults to 50%.
