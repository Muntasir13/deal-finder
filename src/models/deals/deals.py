import os
import uuid

from werkzeug.utils import secure_filename

from common.database import Database
from common.config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
import models.deals.error as DealError


class Deals(object):
    def __init__(self, title, category, link, image, price, _id=None):
        self.title = title
        self.category = category
        self.link = link
        self.image = image
        self.price = price
        self._id = uuid.uuid4().hex if _id is None else _id

    @staticmethod
    def search_by_category(category):
        return Database.find("deals", query={"category": category})

    @staticmethod
    def search_by_name(name):
        name_text = Database.find("deals", query={"category": {"$regex": name}})
        if name_text is not None:
            return name_text

        name_text = Database.find("deals", query={"title": {"$regex": name}})
        if name_text is not None:
            return name_text

    @staticmethod
    def deal_upload(title, category, link, image, price):
        file = image.filename

        if not file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            raise DealError.FileTypeError("File type not supported")

        f = secure_filename(file)
        image_file = os.path.join(UPLOAD_FOLDER, f).replace("\\", "/")
        image.save(image_file)

        Deals(title, category, link, f, price).save_to_db()

        return True

    @staticmethod
    def featured_deals():
        distinct = Database.find_distinct("deals", {}, "category")
        datab = []
        for data in distinct:
            datab += Database.find("deals", query={"category": data}).limit(2)

        return datab

    def save_to_db(self):
        Database.insert("deals", self.json())

    def json(self):
        return {
            "_id": self._id,
            "title": self.title,
            "category": self.category,
            "link": self.link,
            "image": self.image,
            "price": self.price
        }
