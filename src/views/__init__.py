from flask import Flask


def init_app(app: Flask):
    from src.views.card_view import bp_card

    app.register_blueprint(bp_card)

    from src.views.tag_view import bp_tag

    app.register_blueprint(bp_tag)