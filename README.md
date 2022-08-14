# Arrow-Orientation-Detection
Detects whether the arrow is pointing Right, Left, Up or Down and its distance from the camera using OpenCV

# How to use?
1. utils.py is a self made module with all the important functions. 
2. ArrowDetectionMod.py is directly detecting the arrow and finding the Direction along with its distance from camera(using custom 
   aperture and focal length for camera).But in the other file 1st it detects a Box and creates it the Region of Interest and in that box detects the orientation and distance of the arrow.
3. Use the Arrow.jpg provided for best results.

The main aim of this scripts was to mind the distance of direction given for navigation of a remotely controlled locomotive.
