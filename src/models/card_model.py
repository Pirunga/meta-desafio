from . import db

class CardModel(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String, nullable=False)
    data_criacao = db.Column(db.String, nullable=False)
    data_modificacao = db.Column(db.String, nullable=False)

    tag_list = db.relationship(
        'TagModel',
        lazy='joined',
        backref=db.backref('card_list', lazy='joined'),
        secondary='card_tag',
    )