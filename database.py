from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime

db = SQLAlchemy()


class Place(db.Model):
    __tablename__ = "places"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    photo_url = db.Column(db.String(256))
    category = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)

    reviews = db.relationship(
        "Review",
        backref="place",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    @property
    def average_rating(self):
        avg = (
            db.session.query(func.avg(Review.rating))
            .filter_by(place_id=self.id)
            .scalar()
        )
        return round(avg, 2) if avg else None


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)

    place_id = db.Column(
        db.Integer,
        db.ForeignKey("places.id"),
        nullable=False
    )

    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    author = db.Column(db.String(32))
    date = db.Column(db.DateTime, default=datetime.utcnow)
