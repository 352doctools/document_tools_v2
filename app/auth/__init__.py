import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from flask import Blueprint
auth = Blueprint('auth', __name__)
import views



