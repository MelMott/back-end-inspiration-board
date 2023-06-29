from app import db

# "one" side, one Board has many cards
class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", back_populates="board")

# info going back to database
    def to_dict(self):
        return {
            "board_id": self.board_id,
            "title": self.title,
            "owner": self.owner
        }

# info required for create
    @classmethod
    def from_dict(cls, board_details):
        new_board = cls(
            title=board_details["title"],
            owner=board_details["owner"]
        )
        return new_board
