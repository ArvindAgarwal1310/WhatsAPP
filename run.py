from flask import Flask
from .config import load_configurations, configure_logging
from .views import webhook_blueprint

def create_app():
    app = Flask(__name__)

    # Load configurations and logging settings
    load_configurations(app)
    configure_logging()

    # Import and register blueprints, if any
    app.register_blueprint(webhook_blueprint)

    return app
if(__name__ == "__main__"):
    #logging.info("Flask app started")
    app = create_app()
    app.run(host="0.0.0.0", port=80)
