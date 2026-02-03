import os

class DevConfig:
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-123")
    DATABASE_PATH = os.path.join(os.getcwd(), "instance", "app.db")

class TestConfig:
    DEBUG = False
    TESTING = True
    SECRET_KEY = "test-key-456"
    DATABASE_PATH = ":memory:"
