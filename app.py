from pathlib import Path

import aiohttp_jinja2
import jinja2
from aiohttp import web 
from aiohttp.web import Application

from lib import views
from lib.models import load_yolo_model, load_resnet_model
from config import Config

lib = Path("lib")

def create_app() -> Application:
    app = Application()

    app['config'] = Config
    
    # setup routes
    app.router.add_static("/static/", lib / "static")
    app.router.add_view("/", views.IndexView, name="index")
    # setup templates
    aiohttp_jinja2.setup(
        app=app,
        loader=jinja2.FileSystemLoader(lib / "templates"),
    )
    
    # Load models
    app["yolo_model"] = load_yolo_model(Config.YOLO_MODEL_PATH)
    app["feature_model"], app["image_features"] = load_resnet_model(Config.RESNET_MODEL_PATH, Config.FEATURES_PATH)

    return app

async def async_create_app() -> Application:
    return create_app()

if __name__ == '__main__':
    app = create_app()
    web.run_app(app, host='localhost', port=8080)