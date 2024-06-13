import os
import torch
from torchvision import transforms
from sklearn.metrics.pairwise import cosine_similarity
from io import BufferedReader, BytesIO
from base64 import b64encode
from typing import List, Tuple

from PIL import Image
from PIL.ImageDraw import Draw


Coords = List[int]  # Coordinates for the bounding box (x1, y1, x2, y2)
Box = Tuple[int, int, int, int]  # Box format for PIL (left, top, right, bottom)


def open_image(image_fp: BufferedReader) -> Image:
    return Image.open(image_fp)

# Define image preprocessing transformations
preprocess = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Function to load and preprocess an image
def load_and_preprocess_image(image):
    img_tensor = preprocess(image)
    img_tensor = img_tensor.unsqueeze(0)  # Add batch dimension
    return img_tensor

# Function to extract features from an image
def extract_features(image, model, device):
    img_tensor = load_and_preprocess_image(image).to(device)
    with torch.no_grad():
        features = model(img_tensor)
    return features.squeeze().cpu().numpy()

# Function to find the closest image and its label
def find_closest_image_and_label(cropped_image, image_features, data_folder, model, device):
    input_features = extract_features(cropped_image, model, device)
    similarities = {}
    for file_name, features in image_features.items():
        similarity = cosine_similarity([input_features], [features])[0][0]
        similarities[file_name] = similarity
    
    if not similarities:
        raise ValueError("No similarities found. Ensure that image features are correctly extracted.")
    
    closest_image = max(similarities, key=similarities.get)
    label_file = os.path.splitext(closest_image)[0] + '.txt'
    with open(os.path.join(data_folder, label_file), 'r') as f:
        label = f.read().strip()
    return closest_image, label


class PolygonDrawer:
    def __init__(self, image: Image) -> None:
        self._clean_image = image.copy()
        self._image = image
        self._draw = Draw(image)

    @staticmethod
    def coords_to_box(coords: Coords) -> Box:
        """Convert coordinates to PIL box format"""
        return coords[0], coords[1], coords[2], coords[3]

    def highlight_word(self, coords: Coords, word: str) -> None:
        """Add polygon at given coords and add word"""
        box = self.coords_to_box(coords)
        self._draw.rectangle(box, outline="red", width=2)
        text_height = 12  # px, hardcoded
        x, y = box[:2]
        self._draw.text((x, y - text_height), word, fill="red")

    def highlight_box(self, coords: Coords) -> None:
        """Highlight the box and add a label above it"""
        x1, y1, x2, y2 = coords
        self._draw.rectangle([x1, y1, x2, y2], outline="red", width=2)

    def crop(self, coords: Coords) -> Image:
        """Get cropped Image part"""
        box = self.coords_to_box(coords)
        return self._clean_image.crop(box)

    def get_highlighted_image(self) -> Image:
        """Get result Image with highlights"""
        return self._image


def image_b64encode(image: Image) -> str:
    with BytesIO() as io:
        image.save(io, format="png", quality=100)
        io.seek(0)
        return b64encode(io.read()).decode()


def image_to_img_src(image: Image) -> str:
    return f"data:image/png;base64,{image_b64encode(image)}"
