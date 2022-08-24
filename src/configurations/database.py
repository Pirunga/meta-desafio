from flask.app import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_app(app: Flask):
    db.init_app(app)
    app.db = db

    from src.models.tag_model import TagModel
    from src.models.card_model import CardModel
    from src.models.card_tag_model import CardTagModel
