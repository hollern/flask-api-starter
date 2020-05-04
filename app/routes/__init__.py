from flask import Blueprint

blueprint = Blueprint('routes', __name__, url_prefix='/api/v1')

from app.routes import company
from app.routes import errors
from app.routes import user

from app.routes import property
from app.routes import report
from app.routes import unit
