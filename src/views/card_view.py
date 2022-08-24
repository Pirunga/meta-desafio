from flask import Blueprint, request, current_app

from src.models.tag_model import TagModel
from src.models.card_model import CardModel
from src.models.card_tag_model import CardTagModel
from src.static.response import Response
from src.utils.date import Date
from src.static.messages import CARD_CREATED, CARD_NOT_FOUND, CARD_SUCCESS


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


@bp_card.route('/<int:card_id>', methods=['GET'])
def get_card(card_id):
    """
    Get card with specific id.

    :param int card_id: Id of card to delete.
    """
    try:
        card: CardModel = CardModel.query.get(card_id)

        return response.success(CARD_SUCCESS.format('encontrado'), card)
    except AttributeError:
        return response.failed(CARD_NOT_FOUND)


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
        if tag_founded := TagModel.query.filter_by(name=tag.uppercase()).first():
            card_tag: CardTagModel = CardTagModel(card_id=new_card.id, tag_id=tag_founded.id)

            session.add_all([new_card, card_tag])
            session.commit()
    
    session.commit()

    return response.success(CARD_CREATED)


@bp_card.route('/<int:card_id>', methods=['DELETE'])
def remove_card(card_id):
    """
    Delete Card.
    
    :param int card_id: Id of card to delete.
    """
    session = current_app.db.session

    card: CardModel = CardModel.query.get(card_id)

    if not card:
        return response.failed(CARD_NOT_FOUND)
    
    session.delete(card)
    session.commit()

    return response.success(CARD_SUCCESS.format('deletado'))


@bp_card.route('/<int:card_id>', methods=['PUT'])
def update_card(card_id):
    """
    Update Card.
    
    :param int card_id: Id of card to update.
    """
    body = request.get_json()
    session = current_app.db.session

    card: CardModel = CardModel.query.get(card_id)

    if not card:
        return response.failed(CARD_NOT_FOUND)

    card.texto = body.get('texto')
    card.data_modificacao = date.datetime_now(True)

    card_tags: CardTagModel = CardTagModel.query.filter(card_id=card.id).all()

    if card_tags:
        for card_tag in card_tags:
            session.delete(card_tag)
    
    if tags := body.get('tags'):
        for tag in tags:
            if tag_founded := TagModel.query.filter_by(name=tag.uppercase()).first():
                card_tag: CardTagModel = CardTagModel(card_id=card.id, tag_id=tag_founded.id)

                session.add_all([card, card_tag])
                session.commit() 
    
    session.add(card)
    session.commit()

    return response.success(CARD_SUCCESS.format('atualizado'))