from flask import Blueprint

exceptions = Blueprint("exceptions", __name__, template_folder="templates")

from . import handlers  
