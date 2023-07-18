from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy import inspect, asc
from app.models.card import Card
from app import db
from app.routes.routes_helper import get_valid_item_by_id

# POST, GET, and DELETE cards

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# display cards of a board
@cards_bp.route("", methods=['GET'])
def handle_cards():
    title_query = request.args.get("title")
    if title_query:
        cards = Card.query.filter_by(title=title_query)
    else:
        cards = Card.query.order_by(asc(Card.card_id)).all()
    cards_response = []
    for card in cards:
        cards_response.append(card.to_dict())
    return jsonify(cards_response), 200

# create new card 
@cards_bp.route("", methods=['POST'])
def create_card():
    # Get the data from the request body
    request_body = request.get_json()

    # Use it to make an Card
    new_card = Card.from_dict(request_body)

    # Persist (save, commit) it in the database
    db.session.add(new_card)
    db.session.commit()

    # Give back our response
    return {
        "card_id": new_card.card_id,
        "message": new_card.message,
        "msg": "Successfully created"
    }, 201

#  delete card from board 
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
    card_to_delete = get_valid_item_by_id(Card, card_id)

    db.session.delete(card_to_delete)
    db.session.commit()

    return f"Card {card_to_delete.message} is deleted!", 200

# update like count on card 
@cards_bp.route("/<card_id>", methods=["PATCH"])
def update_likes_count(card_id):
    card_to_update = get_valid_item_by_id(Card, card_id)

    request_body = request.get_json()
    
    card_to_update.likes_count = request_body["likes_count"]

    db.session.commit()

    return f"Card {card_id} like count updated to {card_to_update.likes_count}", 200 


