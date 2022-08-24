from flask import Blueprint, request, current_app

from src.models.tag_model import TagModel
from src.models.card_model import CardModel
from src.models.card_tag_model import CardTagModel
from src.static.messages import TAG_ALREADY_EXISTS, TAG_CREATED, TAG_NOT_FOUND, TAG_SUCCESS
from src.static.response import Response


bp_tag = Blueprint('tag_view', __name__, url_prefix='/tag')
response = Response()


@bp_tag.route('/', methods=['POST'])
def create_tag():
    """
    Create tag.
    """
    name = request.get_json().get('name')
    session = current_app.db.session

    if CardModel.query.filter_by(name=name.uppercase()).first():
        return response.conflict(TAG_ALREADY_EXISTS)

    new_card: CardModel = CardModel(name=name.uppercase())

    session.add(new_card)
    session.commit()

    return response.success(TAG_CREATED)


@bp_tag.route('/<int:tag_id>', methods=['GET'])
def get_card(tag_id):
    """
    Get tag with specific id.

    :param int tag_id: Id of tag to delete.
    """
    try:
        tag: TagModel = TagModel.query.get(tag_id)

        return response.success(TAG_SUCCESS.format('encontrado'), tag)

    except AttributeError:
        return response.failed(TAG_NOT_FOUND)


@bp_tag.route('/<int:tag_id>', methods=['DELETE'])
def remove_tag(tag_id):
    """
    Delete Tag.
    
    :param int tag_id: Id of tag to delete.
    """
    session = current_app.db.session

    tag: TagModel = TagModel.query.get(tag_id)

    if not tag:
        return response.failed(TAG_NOT_FOUND)
    
    session.delete(tag)
    session.commit()

    return response.success(TAG_SUCCESS.format('deletada'))


@bp_tag.route('/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id):
    """
    Update Tag.
    
    :param int tag_id: Id of tag to update.
    """
    body = request.get_json()
    session = current_app.db.session

    tag: TagModel = TagModel.query.get(tag_id)

    if not tag:
        return response.failed(TAG_NOT_FOUND)

    tag.texto = body.get('name')

    session.add(tag)
    session.commit()

    return response.success(TAG_SUCCESS.format('atualizadA'))