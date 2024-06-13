from aiohttp.web import Response, View
from aiohttp_jinja2 import render_template
from PIL import Image
import os
import torch

from lib.image import image_to_img_src, PolygonDrawer, find_closest_image_and_label, open_image

class IndexView(View):
    template = "index.html"

    async def get(self) -> Response:
        ctx = {}
        return render_template(self.template, self.request, ctx)

    async def post(self) -> Response:
        try:
            form = await self.request.post()
            image = open_image(form["image"].file)
            yolo_model = self.request.app["yolo_model"]
            feature_model = self.request.app["feature_model"]
            image_features = self.request.app["image_features"]
            data_folder = self.request.app["config"].DATA_FOLDER

            # Detect objects using YOLO
            results = yolo_model(image)
            draw = PolygonDrawer(image)
            labels = []

            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    # Check the structure of the coordinates
                    print(f"Coordinates: {x1, y1, x2, y2}")

                    cropped_img = draw.crop((x1, y1, x2, y2))
                    
                    # Find the closest image and its label for the cropped image
                    closest_image, label = find_closest_image_and_label(
                        cropped_img, image_features, data_folder, feature_model, torch.device("cuda" if torch.cuda.is_available() else "cpu")
                    )

                    # Encode the cropped image to base64
                    cropped_img_b64 = image_to_img_src(cropped_img)
                    
                    # Append the image and label to the list
                    labels.append({"image": cropped_img_b64, "label": label})

            # Encode the full image with highlighted boxes
            image_b64 = image_to_img_src(draw.get_highlighted_image())
            ctx = {"image": image_b64, "labels": labels}

        except Exception as err:
            error_type = type(err).__name__
            ctx = {"error": str(err), "error_type": error_type}

        return render_template(self.template, self.request, ctx)
