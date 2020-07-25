import os
import sys

import argparse
from ..Training.src.keras_yolo3.yolo import YOLO, detect_video


from PIL import Image
from timeit import default_timer as timer

from ..Utils.utils import load_extractor_model, load_features, parse_input, detect_object

#import utils

import pandas as pd
import numpy as np
import random
import test

from ..Utils.Get_File_Paths import GetFileList



# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# returns the directory level that can access whatever file we need
def get_parent_dir(n=1):
    """ returns the n-th parent dicrectory of the current
    working directory """
    current_path = os.path.dirname(os.path.abspath(__file__))
    for k in range(n):
        current_path = os.path.dirname(current_path)
    return current_path

# src_path = os.path.join(get_parent_dir(1), "Training", "src")
# utils_path = os.path.join(get_parent_dir(1), "Utils")

# sys.path.append(src_path)
# sys.path.append(utils_path)

# # Set up folder names for default values
# data_folder = os.path.join(get_parent_dir(n=1), "Data")

# image_folder = os.path.join(data_folder, "Source_Images")

# image_test_folder = os.path.join(image_folder, "Test_Images")

# detection_results_folder = os.path.join(image_folder, "Test_Image_Detection_Results")
# detection_results_file = os.path.join(detection_results_folder, "Detection_Results.csv")

# model_folder = os.path.join(data_folder, "Model_Weights")

# model_weights = os.path.join(model_folder, "trained_weights_final.h5")
# model_classes = os.path.join(model_folder, "data_classes.txt")

# anchors_path = os.path.join(src_path, "keras_yolo3", "model_data", "yolo_anchors.txt")

class MySignDetector:
    def __init__(self, min_threshold=0.1,stopBool=False):
        print('shit')
               # Delete all default flags
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3" # i didnt know where to put this line so here it is
        self.min_threshold = min_threshold
        self.FLAGS = None
        self.parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
        self.stopBool = stopBool

        self.src_path = os.path.join(get_parent_dir(1), "Training", "src")
        self.utils_path = os.path.join(get_parent_dir(1), "Utils")

        sys.path.append(self.src_path)
        sys.path.append(self.utils_path)

        # Set up folder names for default values
        self.data_folder = os.path.join(get_parent_dir(n=1), "Data")

        self.image_folder = os.path.join(self.data_folder, "Source_Images")

        self.image_test_folder = os.path.join(self.image_folder, "Test_Images")

        self.detection_results_folder = os.path.join(self.image_folder, "Test_Image_Detection_Results")
        self.detection_results_file = os.path.join(self.detection_results_folder, "Detection_Results.csv")

        self.model_folder = os.path.join(self.data_folder, "Model_Weights")

        self.model_weights = os.path.join(self.model_folder, "trained_weights_final.h5")
        self.model_classes = os.path.join(self.model_folder, "data_classes.txt")

        self.anchors_path = os.path.join(self.src_path, "keras_yolo3", "model_data", "yolo_anchors.txt")
         
        print('more shit to ensure that everyhting has run smoothly')  
        """
        Command line options
        """
        self.parser.add_argument(
            "--input_path",
            type=str,
            default=self.image_test_folder,
            help="Path to image/video directory. All subdirectories will be included. Default is "
            + self.image_test_folder,
        )

        self.parser.add_argument(
            "--output",
            type=str,
            default=self.detection_results_folder,
            help="Output path for detection results. Default is "
            + self.detection_results_folder,
        )

        self.parser.add_argument(
            "--no_save_img",
            default=False,
            action="store_true",
            help="Only save bounding box coordinates but do not save output images with annotated boxes. Default is False.",
        )

        self.parser.add_argument(
            "--file_types",
            "--names-list",
            nargs="*",
            default=[],
            help="Specify list of file types to include. Default is --file_types .jpg .jpeg .png .mp4",
        )

        self.parser.add_argument(
            "--yolo_model",
            type=str,
            dest="model_path",
            default=self.model_weights,
            help="Path to pre-trained weight files. Default is " + self.model_weights,
        )

        self.parser.add_argument(
            "--anchors",
            type=str,
            dest="anchors_path",
            default=self.anchors_path,
            help="Path to YOLO anchors. Default is " + self.anchors_path,
        )

        self.parser.add_argument(
            "--classes",
            type=str,
            dest="classes_path",
            default=self.model_classes,
            help="Path to YOLO class specifications. Default is " + self.model_classes,
        )

        self.parser.add_argument(
            "--gpu_num", type=int, default=1, help="Number of GPU to use. Default is 1"
        )

        self.parser.add_argument(
            "--confidence",
            type=float,
            dest="score",
            default=self.min_threshold,
            help="Threshold for YOLO object confidence score to show predictions. Default is 0.25.",
        )

        self.parser.add_argument(
            "--box_file",
            type=str,
            dest="box",
            default=self.detection_results_file,
            help="File to save bounding box results to. Default is "
            + self.detection_results_file,
        )

        self.parser.add_argument(
            "--postfix",
            type=str,
            dest="postfix",
            default="_imstupid",
            help='Specify the postfix for images with bounding boxes. Default is "_catface"',
        )

        self.FLAGS = self.parser.parse_args()

        self.save_img = not self.FLAGS.no_save_img

        self.file_types = self.FLAGS.file_types

        if self.file_types:
            self.input_paths = GetFileList(self.FLAGS.input_path, endings=selffile_types)
        else:
            self.input_paths = GetFileList(self.FLAGS.input_path)

        # Split images and videos
        self.img_endings = (".jpg", ".jpg", ".png")
        #vid_endings = (".mp4", ".mpeg", ".mpg", ".avi")

        self.input_image_paths = []
        #input_video_paths = []

        for item in self.input_paths:
            if item.endswith(self.img_endings):
                self.input_image_paths.append(item)
            #elif item.endswith(vid_endings):
                #input_video_paths.append(item)

        self.output_path = self.FLAGS.output
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        self.yolo = YOLO(
            **{
            "model_path": self.FLAGS.model_path,
            "anchors_path": self.FLAGS.anchors_path,
            "classes_path": self.FLAGS.classes_path,
            "score": self.FLAGS.score,
            "gpu_num": self.FLAGS.gpu_num,
            "model_image_size": (416, 416),
            }
        )
        
        self.out_df = pd.DataFrame(
            columns=[
                "image",
                "image_path",
                "xmin",
                "ymin",
                "xmax",
                "ymax",
                "label",
                "confidence",
                "x_size",
                "y_size",
            ]
        )

        self.class_file = open(self.FLAGS.classes_path, "r")
        self.input_labels = [line.rstrip("\n")  for line in self.class_file.readlines()]
        print("Found {} input labels: {} ...".format(len(self.input_labels), self.input_labels))


    def checkForSigns(self, img):
        # run the image through the model, call self.generate()?
        # self.generate() returns boxes, scores, classes variables
        
        pred, img_array = detect_object(self.yolo, img, True)
        
        # print(pred)
        # print(img_array)
        
        for item in pred:
            if item[5] > self.min_threshold:
                return True
            
        return False

        print(self.yolo.boxes) 
        #i think this is wrong
        # check if there are more than 0 boxes found (boxes var from the yolo class)
        # assig/n boolean to dict based on number of boxes
        # return and close session 
        
        #return if boxes > 0
        #sign key, true false???
