import uuid
import models.users.errors as UserErrors

from common.database import Database
from common.utils import Utils


class Users(object):
    def __init__(self, username, email, password, user_type, institution=None, _id=None):
        self.username = username
        self.email = email
        self.password = password
        self.user_type = user_type
        self.institution = institution
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<{} {}>".format(self.user_type, self.email)

    @staticmethod
    def login_is_valid(username, password):
        user_data = Database.find_one("users", {"username": username})
        if user_data is None:
            raise UserErrors.UserNotExistError("The username doesn't exist")

        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("Incorrect password")

        return True

    @staticmethod
    def register_user(username, email, password, confirm_pass, user_type, institution=None):
        user_data = Database.find_one("users", {"username": username})

        if user_data is not None:
            raise UserErrors.UserAlreadyExistsError("This username already exists. Try using a different username")

        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailFormat("Wrong email format")

        if not password == confirm_pass:
            raise UserErrors.PasswordMatchError("Passwords don't match")

        if institution is None:
            Users(username, email, Utils.hash_password(password), user_type).save_to_db_user()

        elif institution is not None:
            Users(username, email, Utils.hash_password(password), user_type, institution).save_to_db_owner()

        return True

    @staticmethod
    def get_by_email(username, email):
        user_data = Database.find_one("users", query={"username": username,
                                                      "email": email})
        if user_data is None:
            raise UserErrors.UserNotExistError("This username doesn't exist")

        return True

    @staticmethod
    def update_password(username, password, confirm_pass):
        if not password == confirm_pass:
            raise UserErrors.PasswordMatchError("Passwords don't match")

        Database.update_one("users", {"username": username}, {"password": Utils.hash_password(password)})

        return True

    def save_to_db_user(self):
        Database.insert("users", self.json_user())

    def save_to_db_owner(self):
        Database.insert("users", self.json_owner())

    def json_user(self):
        return{
            "_id": self._id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "user_type": self.user_type
        }

    def json_owner(self):
        return{
            "_id": self._id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "institution": self.institution,
            "user_type": self.user_type
        }
