from flask import Flask, render_template, request, redirect, url_for, flash
from database import db, Place, Review
import magic
import os
import uuid

from config import Config


def allowed_file(file):
    if not file:
        return False
    mime = magic.from_buffer(file.read(2048), mime=True)
    file.seek(0)
    return mime in app.config["ALLOWED_MIME_TYPES"]


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    category = request.args.get("category")
    if category:
        places = Place.query.filter_by(category=category).all()
    else:
        places = Place.query.all()

    categories = db.session.query(Place.category).distinct().all()
    categories = [c[0] for c in categories]

    return render_template(
        "index.html",
        places=places,
        selected_category=category,
        categories=categories,
    )


@app.route("/place/new", methods=["GET", "POST"])
def new_place():
    if request.method == "POST":
        name = request.form["name"]
        address = request.form["address"]
        category = request.form["category"]
        description = request.form.get("description")

        file = request.files.get("photo")
        photo_url = None

        if file and allowed_file(file):
            ext = os.path.splitext(file.filename)[1]
            filename = f"{uuid.uuid4().hex}{ext}"
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            photo_url = url_for("static", filename=f"uploads/{filename}")
        else:
            flash("Недопустимый формат изображения")
            return redirect(url_for("new_place"))

        if not name or not address or not category:
            flash("Название, адрес и категория обязательны")
            return redirect(url_for("new_place"))

        place = Place(
            name=name,
            address=address,
            category=category,
            description=description,
            photo_url=photo_url,
        )
        db.session.add(place)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("new_place.html")


@app.route("/place/<int:place_id>", methods=["GET", "POST"])
def place_detail(place_id):
    place = Place.query.get_or_404(place_id)

    if request.method == "POST":
        rating = int(request.form["rating"])
        comment = request.form.get("comment")
        author = request.form.get("author")

        if rating >= 1 and rating <= 5:
            review = Review(
                place=place,
                rating=rating,
                comment=comment,
                author=author
            )

            db.session.add(review)
            db.session.commit()
            return redirect(url_for("place_detail", place_id=place_id))

    reviews = place.reviews.order_by(Review.date.desc()).all()
    avg = place.average_rating

    return render_template(
        "place.html",
        place=place,
        reviews=reviews,
        average=avg
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
