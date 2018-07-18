from flask import Blueprint

statistics = Blueprint('statistics', __name__, url_prefix='/statistics')

from . import views