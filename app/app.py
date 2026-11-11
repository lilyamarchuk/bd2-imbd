from my_project import create_app

app = create_app()

if __name__ == "__main__":
    cfg = app.config["APP_CONFIG"]["app"]
    app.run(host=cfg.get("host", "0.0.0.0"), port=cfg.get("port", 5000), debug=cfg.get("debug", False))
