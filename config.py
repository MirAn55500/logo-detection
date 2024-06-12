import os

class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    YOLO_MODEL_PATH = os.path.join(BASE_DIR, 'weights', 'best.pt')
    RESNET_MODEL_PATH = os.path.join(BASE_DIR, 'weights', 'resnet50_feature_extractor.pth')
    FEATURES_PATH = os.path.join(BASE_DIR, 'weights', 'image_features.pkl')
    DATA_FOLDER = os.path.join(BASE_DIR, 'data_folder')
