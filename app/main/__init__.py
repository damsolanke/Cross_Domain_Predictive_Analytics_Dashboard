from flask import Blueprint

main = Blueprint('main', __name__)

# Register analytics controller
from . import routes
from app.main.analytics_controller import analytics
main.register_blueprint(analytics)