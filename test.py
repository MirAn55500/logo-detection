import os
import torch
from PIL import Image
from ultralytics import YOLO

from lib.image import PolygonDrawer, find_closest_image_and_label, image_to_img_src
from lib.models import load_yolo_model, load_resnet_model
from config import Config

def main():
    # Load models
    yolo_model = load_yolo_model(Config.YOLO_MODEL_PATH)
    feature_model, image_features = load_resnet_model(Config.RESNET_MODEL_PATH, Config.FEATURES_PATH)

    # Load and preprocess the image
    input_image_path = '/home/ammironov.ext/logo-detection/data_folder/3m2_cropped_0.png'
    image = Image.open(input_image_path)

    draw = PolygonDrawer(image)

    # Detect objects using YOLO
    results = yolo_model(image)
    labels = []

    for result in results:
        for box in result.boxes:
            # Unpack bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Adjust if necessary based on your bounding box structure
            cropped_img = draw.crop((x1, y1, x2, y2))
            
            # Find the closest image and its label for the cropped image
            closest_image, label = find_closest_image_and_label(
                cropped_img, image_features, Config.DATA_FOLDER, feature_model, torch.device("cuda" if torch.cuda.is_available() else "cpu")
            )
            
            # Highlight the detected box with label
            draw.highlight_box((x1, y1, x2, y2))
            
            # Append the result to the labels list
            labels.append({"closest_image": closest_image, "label": label})

            # Optionally save or display the cropped image
            cropped_img_b64 = image_to_img_src(cropped_img)
            print(f"Cropped Image Base64: {cropped_img_b64}")
            print(f"Label: {label}")

    # Display or save the final processed image with highlighted boxes
    processed_image_path = 'processed_image.jpg'
    draw.get_highlighted_image().save(processed_image_path)
    print(f"Processed image saved to {processed_image_path}")

if __name__ == '__main__':
    main()
