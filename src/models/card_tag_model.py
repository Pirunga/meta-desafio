from . import db


class CardTagModel(db.Model):
    __tablename__ = 'card_tag'

    id = db.Column(db.Integer, primary_key=True)

    card_id = db.Column(
        db.Integer,
        db.ForeignKey('cards.id', onupdate='CASCADE', ondelete='CASCADE',),
        nullable=False,
    )

    tag_id = db.Column(
        db.Integer,
        db.ForeignKey('tags.id', onupdate='CASCADE', ondelete='CASCADE',),
        nullable=False,
    )