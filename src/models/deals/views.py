from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

from models.deals.deals import Deals
import models.deals.error as DealError

deals_blueprint = Blueprint('deals', __name__)


@deals_blueprint.route('/upload_deal', methods=['GET', 'POST'])
def upload_deal():
    if request.method == 'POST':
        title = request.form.get("title", None)
        category = request.form.get("category")
        price = request.form.get("price", None)
        link = request.form.get("link", None)
        image = request.files.get("image", None)

        try:
            if Deals.deal_upload(title, category, link, image, price):
                return redirect(url_for('index'))
        except DealError.DealError as e:
            return e.message

    return render_template("add_deal.html")


@deals_blueprint.route('/deals/<string:category>')
def deals_by_category(category):
    deals_data = Deals.search_by_category(category)
    return render_template("deals.html", deals=deals_data)
