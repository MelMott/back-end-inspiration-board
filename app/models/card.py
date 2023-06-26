from app import db

# Inherits from the Model class! The model class is accessed through db...
class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)

    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))
    board = db.relationship("Board", back_populates="cards")


    def to_dict(self):
        return {
            "card_id": self.card_id,
            "message": self.message,
            "likes_count": self.likes_count,
            "board_id": self.board_id
        }

    @classmethod
    def from_dict(cls, card_details):
        new_card = cls(
            message=card_details["message"],
            likes_count=card_details["likes_count"],
            board_id=card_details["board_id"]
        )
        return new_card

