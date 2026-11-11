import os
import yaml

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "config", "app.yml")


def load_config(path=None):
    with open(path or DEFAULT_PATH, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    db = cfg["database"]
    db["user"] = os.getenv("DB_USER", db["user"])
    db["password"] = os.getenv("DB_PASSWORD", db["password"])
    db["host"] = os.getenv("DB_HOST", db["host"])
    db["port"] = int(os.getenv("DB_PORT", db["port"]))
    db["name"] = os.getenv("DB_NAME", db["name"])
    return cfg


def build_db_uri(cfg):
    d = cfg["database"]
    return f"{d['driver']}://{d['user']}:{d['password']}@{d['host']}:{d['port']}/{d['name']}?charset=utf8mb4"
