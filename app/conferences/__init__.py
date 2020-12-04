from flask import Blueprint

bp = Blueprint('conferences', __name__)

from app.conferences import routes
