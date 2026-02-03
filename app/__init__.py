from __future__ import annotations

import os
from pathlib import Path

from flask import Flask

from .config import DevConfig, TestConfig
from .db import close_db, init_db_command
from .routes_api import bp as api_bp
from .routes_ui import bp as ui_bp

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

    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

    with app.app_context():
        from .db import get_db, init_db

        try:
            db = get_db()
            db.execute("SELECT 1 FROM tasks LIMIT 1")
        except Exception:
            init_db()
            print("Database initialized.")

    return app
