import torch
import torch.nn as nn
from torchvision import models
from torchvision.models import ResNet50_Weights
from typing import Tuple
from ultralytics import YOLO
import pickle

def load_yolo_model(model_path: str) -> YOLO:
    return YOLO(model_path)

def load_resnet_model(model_path: str, features_path: str) -> Tuple[nn.Module, dict]:
    model = models.resnet50(weights=ResNet50_Weights.DEFAULT)
    model = nn.Sequential(*list(model.children())[:-1])
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    model = model.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

    with open(features_path, 'rb') as f:
        image_features = pickle.load(f)

    return model, image_features

