# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import argparse
import glob
import multiprocessing as mp
import os
import time
import cv2
import tqdm

from detectron2.data.detection_utils import read_image
from detectron2.utils.logger import setup_logger

from predictor import VisualizationDemo
from shapely.geometry import Point, Polygon

from adet.config import get_cfg

# constants
WINDOW_NAME = "COCO detections"


def setup_cfg(args):
    # load config from file and command-line arguments
    cfg = get_cfg()
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    # Set score_threshold for builtin models
    # cfg.MODEL.RETINANET.SCORE_THRESH_TEST = args.confidence_threshold
    # cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = args.confidence_threshold
    # cfg.MODEL.FCOS.INFERENCE_TH_TEST = args.confidence_threshold
    # cfg.MODEL.MEInst.INFERENCE_TH_TEST = args.confidence_threshold
    # cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = args.confidence_threshold
    cfg.freeze()
    return cfg


def get_parser():
    parser = argparse.ArgumentParser(description="Detectron2 Demo")
    parser.add_argument(
        "--config-file",
        default="configs/quick_schedules/e2e_mask_rcnn_R_50_FPN_inference_acc_test.yaml",
        metavar="FILE",
        help="path to config file",
    )
    parser.add_argument("--webcam", action="store_true", help="Take inputs from webcam.")
    parser.add_argument("--video-input", help="Path to video file.")
    parser.add_argument("--input", nargs="+", help="A list of space separated input images")
    parser.add_argument(
        "--output",
        help="A file or directory to save output visualizations. "
        "If not given, will show output in an OpenCV window.",
    )

    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.3,
        help="Minimum score for instance predictions to be shown",
    )
    parser.add_argument(
        "--opts",
        help="Modify config options using the command-line 'KEY VALUE' pairs",
        default=[],
        nargs=argparse.REMAINDER,
    )
    return parser

#function to check if a centrepoint of a bounding box is inside a polygon
def compare_polygon_bbox(centre_point, polygon_points):
    """ 
    Inputs:
        centre_point: tuple of (x,y) coordinates of the centre point of the bounding box
        polygon_points: list of tuples of (x,y) coordinates of the polygon
    Output:
        True if the centre point is inside the polygon, False otherwise
    """
    #create a polygon object
    polygon = Polygon(polygon_points)
    #create a point object
    point = Point(centre_point)
    #check if the point is inside the polygon
    return point.within(polygon)


# for a given frame, we compare the predicted results with the ground truth results. predicted results has the following format:
#   [{"file_name": 'image1.jpg', "outputs": [{"polygon": [[x1,y1],[x2,y2],...,[xn,yn]], "recognition": "text1", "score": 0.9, "cntrl_points": [[x1,y1],[x2,y2],...,[xn,yn]]},...]
# ground truth results have the following format:

def compare_predicted_polys_to_ground_truth(original_polygon_points_list, predicted_polygon_points_list):
    pass



def get_detector_score(original_polygon_points_list, predicted_polygon_points_list):
    """
    Inputs:
        original_polygon_points_list: list of polygons (ground truth). Each polygon is a list of tuples of (x,y) coordinates
        predicted_polygon_points_list: list of polygons (predicted). Each polygon is a list of tuples of (x,y) coordinates
    Output:
        detector_score: float between 0 and 1. 1 means the predicted polygon is exactly the same as the original polygon
    """
    catch = 0
    miss = 0
    
    # extract centre coordinates from each polygon in original_polygon_points_list
    for polygon in original_polygon_points_list:
        # TODO: calculate centroid using the points in polygon
        centre_point = polygon[0]
        # check if centre point is inside the predicted polygon
        for predicted_polygon in predicted_polygon_points_list:
            if centre_point in predicted_polygon:
                catch += 1
                
    miss = len(original_polygon_points_list) - catch
    detector_score = catch / (catch + miss)
    return detector_score, catch, miss


if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    args = get_parser().parse_args()
    logger = setup_logger()
    logger.info("Arguments: " + str(args))

    cfg = setup_cfg(args)

    demo = VisualizationDemo(cfg)
    
    if args.input:
        if os.path.isdir(args.input[0]):
            args.input = [os.path.join(args.input[0], fname) for fname in os.listdir(args.input[0])]
        elif len(args.input) == 1:
            args.input = glob.glob(os.path.expanduser(args.input[0]))
            assert args.input, "The input path(s) was not found"
        
        frame_start = 1
        output_image_list = []
        for path in tqdm.tqdm(args.input, disable=not args.output):
            # use PIL, to be consistent with evaluation
            img = read_image(path, format="BGR")
            start_time = time.time()
            predictions, visualized_output, outputs = demo.run_on_image(img)
            logger.info(
                "{}: detected {} instances in {:.2f}s".format(
                    path, len(predictions["instances"]), time.time() - start_time
                )
            )
            #save the outputs as a list of json. have the name of the image file also as a field in the json.
            # something like this format. get filename from args.input
            # [{"file_name": 'image1.jpg', "outputs": [{"polygon": [[x1,y1],[x2,y2],...,[xn,yn]], "recognition": "text1", "score": 0.9, "cntrl_points": [[x1,y1],[x2,y2],...,[xn,yn]]}, 
            #   {"polygon": [[x1,y1],[x2,y2],...,[xn,yn]], "recognition": "text2", "score": 0.8}, "cntrl_points": [[x1,y1],[x2,y2],...,[xn,yn]], ...]}, 
            #   {"file_name": 'image2.jpg', "outputs": [{"polygon": [[x1,y1],[x2,y2],...,[xn,yn]], "recognition": "text1", "score": 0.9}, 
            #   {"polygon": [[x1,y1],[x2,y2],...,[xn,yn]], "recognition": "text2", "score": 0.8}, ...]}, ...]
            file_name = os.path.basename(path)
            output_image_list.append({"file_name": file_name, "outputs": outputs})
        print(output_image_list)