import jetson.inference
import jetson.utils

import argparse
import sys

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.")

parser.add_argument("input_URI", type=str, default="/dev/video0", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="output.mp4", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

try:
	opt = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

# load the object detection network
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)

# create video sources & outputs
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv)
alert_classes = ["person"]
# process frames until the user exits
while True:
	# capture the next image
	img = input.Capture()
	if img is None:
		print("No image detected", end = "\r")
		continue

	# detect objects in the image (with overlay)
	detections = net.Detect(img, overlay=opt.overlay)
	if len(detections)==0:
		print("No objects in frame", end = "\r")
	for detection in detections: 
		ClassID = detection.ClassID
		Classname = net.GetClassLabel(ClassID)
		if Classname in alert_classes:
			print(f'I detected a {Classname}',end = "\r")
	# to do detect whether object is human or not. 
    #(https://rawgit.com/dusty-nv/jetson-inference/master/docs/html/python/jetson.inference.html#detectNet)
		

	# render the image
	output.Render(img)

	# update the title bar
	output.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))

	# print out performance info
	# net.PrintProfilerTimes()

	# exit on input/output EOS
	if not input.IsStreaming() or not output.IsStreaming():
		break
