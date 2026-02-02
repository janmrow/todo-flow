from __future__ import annotations

import os
from pathlib import Path

from flask import Flask

from .config import DevConfig, TestConfig
from .routes_ui import bp as ui_bp
from .routes_api import bp as api_bp

_CONFIGS = {
    "dev": DevConfig,
    "test": TestConfig,
}


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    env = (config_name or os.getenv("APP_ENV", "dev")).lower()
    config_cls = _CONFIGS.get(env, DevConfig)
    app.config.from_object(config_cls)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    app.config.setdefault("SECRET_KEY", os.getenv("SECRET_KEY", "dev"))

    app.register_blueprint(ui_bp)
    app.register_blueprint(api_bp)
    return app
