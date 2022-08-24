from flask import Blueprint, request, current_app

from src.models.tag_model import TagModel
from src.models.card_model import CardModel
from src.models.card_tag_model import CardTagModel
from src.static.response import Response
from src.utils.date import Date
from src.static.messages import CARD_ALREADY_EXISTS, CARD_CREATED, CARD_NOT_FOUND, CARD_SUCCESS


bp_card = Blueprint('card_view', __name__, url_prefix='/card')
response = Response()
date = Date()


@bp_card.route('/card_by_tags', methods=['POST'])
def list_cards():
    """
    Get cards with specific tag.
    """

    tag = request.get_json().get('tag')
    session = current_app.db.session
    
    cards = []

    if tag := TagModel.query.filter(TagModel.name == tag.uppercase()).first():
        cards = session.query(CardModel).join(CardTagModel).filter(CardTagModel.tag_id == tag.id).all()
    
    if not cards:
        return response.failed(CARD_NOT_FOUND)

    return response.success(CARD_SUCCESS.format('encontrado(s)'), cards)


@bp_card.route('/', methods=['POST'])
def create_card():
    """
    Create card.
    """
    body = request.get_json()
    session = current_app.db.session

    new_card: CardModel = CardModel(
        texto=body.get('texto'), 
        data_criacao=date.datetime_now(True), 
        data_modificacao=date.datetime_now(True)
    )

    session.add(new_card)

    for tag in body.get('tags'):
        if tag_founded := TagModel.query.filter(TagModel.name == tag.uppercase()).first():
            card_tag: CardTagModel = CardTagModel()