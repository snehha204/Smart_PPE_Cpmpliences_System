"""this file is used to download the dataset (vest dataset)
 from the given url and save it to the specified path"""

from roboflow import Roboflow

rf = Roboflow(api_key="oj8Zkm3Yn3YmE2ZDcSGe")
project = rf.workspace("projet-dinitiation-s3gke").project("vest-worker-only-vest")
version = project.version(1)

dataset = version.download("yolov8")

print("Dataset downloaded successfully!")