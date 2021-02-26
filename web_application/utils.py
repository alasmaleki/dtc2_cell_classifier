import io, os , string , random, time, json, glob
from pathlib import Path
from datetime import date, timedelta
from flask import Flask, jsonify, request, render_template,redirect
from PIL import Image
import cv2
import numpy as np
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
from detectron2.data.catalog import Metadata
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.utils.visualizer import ColorMode
from detectron2 import model_zoo
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.modeling import build_model
from detectron2.data.catalog import Metadata




def rand_name():
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(4))
    return result_str

#################################Detectron Model setup########################
def detect(img):
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file('COCO-InstanceSegmentation/mask_rcnn_R_101_FPN_3x.yaml'))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5 # Set threshold for this model
    cfg.MODEL.WEIGHTS = '../model_final.pth' # Set path model .pth
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2
    cfg.MODEL.DEVICE = "cpu"
    predictor = DefaultPredictor(cfg)
    print(img.shape)
    outputs = predictor(img)
    # metadata = MetadataCatalog.get(cfg.DATASETS.TRAIN[0])
    my_metadata = Metadata()
    my_metadata.set(thing_classes = ['cell', 'nucleus'])
    classes = my_metadata.thing_classes

    v = Visualizer(img[:, :, ::-1], metadata=my_metadata, scale=0.5) 
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))

    instances = outputs["instances"]
    scores = instances.get_fields()["scores"].tolist()
    pred_classes = instances.get_fields()["pred_classes"].tolist()
    pred_boxes = instances.get_fields()["pred_boxes"].tensor.tolist()
    response = {
        "scores": scores,
        "pred_classes": pred_classes,
        "pred_boxes" : pred_boxes,
        "classes": classes
    }
    img_name = rand_name()
    cv2.imwrite('static/img/'+img_name+'.jpg' ,out.get_image()[:, :, ::-1])
    return response,img_name

    #################Clean Up###################
 
def cleanup2(path):
    print('path',path)
    time_in_secs = time.time() - (10)
    for root, dirs, files in os.walk(path, topdown=False):
        print(root, dirs, files)
        for file_ in files:
            print('files',file_)
            full_path = os.path.join(root, file_)
            stat = os.stat(full_path)
            print(full_path)
            
            if stat.st_atime <= time_in_secs:
                remove(full_path)
                print('should call remove')
            
        if not os.listdir(root):
            remove(root)
    
def remove(path):
    try:
        if os.path.exists(path):
            os.remove(path)
            print('remo')
    except OSError:
        print ("Unable to remove file: %s" % path)

def cleanup():
    herepath = os.path.dirname(os.path.realpath(__file__))
    files = glob.glob(herepath+'/static/img/*.jpg', recursive=True)
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))