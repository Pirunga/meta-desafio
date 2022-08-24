from flask import Blueprint, request, current_app

from src.models.tag_model import TagModel
from src.models.card_model import CardModel
from src.models.card_tag_model import CardTagModel
from src.static.response import Response
from src.utils.date import Date

bp_tag = Blueprint("tag_view", __name__, url_prefix="/tag")