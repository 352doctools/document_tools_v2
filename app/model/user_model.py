from werkzeug.security import check_password_hash
from flask_login import UserMixin
import json
import uuid
from ..auth import hash

# define profile.json constant, the file is used to
#  save user name and password_hash
PROFILE_FILE = "profiles.json"


class User(UserMixin):
    def __init__(self, uid=None, uname=None, usergroup=None):
        self.uid = uid
        self.uname = uname
        self.usergroup = usergroup

    def to_dict(self):
        return self.__dict__

    def get_id(self):
        return self.uid
