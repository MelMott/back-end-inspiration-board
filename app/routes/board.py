from flask import Blueprint, jsonify, abort, make_response, request
from app import db

from app.models.board import Board
from app.routes.routes_helper import get_valid_item_by_id

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

# display boards
@boards_bp.route("", methods=['GET'])
def handle_boards():
    title_query = request.args.get("title")
    if title_query:
        boards = Board.query.filter_by(title=title_query)
    else:
        boards = Board.query.all()

    boards_response = []
    for board in boards :
        boards_response.append(board.to_dict())
    return jsonify(boards_response), 200

# create new board 
@boards_bp.route("", methods=['POST'])
def create_board():
    request_body = request.get_json()
    new_board = Board.from_dict(request_body)

    db.session.add(new_board)
    db.session.commit()

    # Give back our response
    return {
        "board_id": new_board.board_id,
        "title": new_board.title,
        "owner": new_board.owner,
        "msg": "Successfully created"
    }, 201

# get one board (to display)
@boards_bp.route("/<board_id>", methods=['GET'])
def handle_one_board(board_id):
    board = get_valid_item_by_id(Board, board_id)
    return board.to_dict(), 200

# get all cards of one board 
@boards_bp.route("/<board_id>/cards", methods=['GET'])
def handle_all_cards_of_one_(board_id):
    board = get_valid_item_by_id(Board, board_id)

    cards_response = []
    for card in board.cards:
        cards_response.append(card.to_dict())

    return jsonify(cards_response), 200


# delete one board (by id)
@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_one_board(board_id):
    board_to_delete = get_valid_item_by_id(Board, board_id)

    db.session.delete(board_to_delete)
    db.session.commit()

    return f"Board {board_to_delete.title} is deleted!", 200