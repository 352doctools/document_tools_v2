import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from flask import Blueprint
doc = Blueprint('doc', __name__)
import views



