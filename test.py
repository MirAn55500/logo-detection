import os
import torch
from PIL import Image
from ultralytics import YOLO

from lib.image import find_closest_image_and_label, open_image
from lib.models import load_yolo_model, load_resnet_model
from config import Config

def main():
    # Load models
    yolo_model = load_yolo_model(Config.YOLO_MODEL_PATH)
    feature_model, image_features = load_resnet_model(Config.RESNET_MODEL_PATH, Config.FEATURES_PATH)

    # Load and preprocess the image
    input_image_path = '/home/ammironov.ext/logo-detection/data_folder/3m2_cropped_0.png'
    image = Image.open(input_image_path)

    # Detect objects using YOLO
    results = yolo_model(image)
    labels = []

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cropped_img = image.crop((x1, y1, x2, y2))
            
            # Find the closest image and its label for the cropped image
            closest_image, label = find_closest_image_and_label(
                cropped_img, image_features, Config.DATA_FOLDER, feature_model, torch.device("cuda" if torch.cuda.is_available() else "cpu")
            )

            # Append the closest image and its label to the list
            labels.append({"closest_image": closest_image, "label": label})
    
    # Print the results
    print("Detected Labels and Closest Images:")
    for item in labels:
        print(f"Label: {item['label']}, Closest Image: {item['closest_image']}")

if __name__ == '__main__':
    main()
