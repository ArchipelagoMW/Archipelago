"""API endpoints package."""
from flask import Blueprint

api_endpoints = Blueprint('api', __name__, url_prefix="/api")

from . import generate