from flask import Blueprint

bp = Blueprint('ncaa', __name__)

from app.ncaa import routes
