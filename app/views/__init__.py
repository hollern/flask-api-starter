from flask import Blueprint

blueprint = Blueprint('views', __name__, url_prefix='/')

from app.views import routes
