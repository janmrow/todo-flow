import os


class DevConfig:
    DEBUG = True
    TESTING = False
    DATABASE_PATH = os.path.join(os.getcwd(), "instance", "app.db")


class TestConfig:
    DEBUG = False
    TESTING = True
    DATABASE_PATH = ":memory:"
