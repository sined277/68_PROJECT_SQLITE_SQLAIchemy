from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CREATE TABLE
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


# Create the Book table in the database.
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    ## READ ALL RECORDS
    all_books = db.session.query(Book).all()
    # Render the index.html template and pass in the all_books variable to be displayed in a table.
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # CREATE RECORD
        # Create a new Book object with the data from the form.
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        # Add the new book to the database session and commit the changes.
        db.session.add(new_book)
        db.session.commit()
        # Redirect the user back to the home page.
        return redirect(url_for('home'))
    # Render the add.html template for GET requests.
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        # UPDATE RECORD
        # Get the ID of the book to be updated from the form.
        book_id = request.form['id']
        # Find the Book object with that ID.
        book_to_update = Book.query.get(book_id)
        # Update the rating of the book to the new value from the form.
        book_to_update.rating = request.form['rating']
        # Commit the changes to the database.
        db.session.commit()
        # Redirect the user back to the home page.
        return redirect(url_for('home'))
    # If this is a GET request, get the ID of the book to be edited from the query string.
    book_id = request.args.get('id')
    # Find the Book object with that ID.
    book_selected = Book.query.get(book_id)
    # Render the edit_rating.html template and pass in the book_selected variable to display the current rating and allow the user to edit it.
    return render_template("edit_rating.html", book=book_selected)


@app.route("/delete")
def delete():
    # Get the ID of the book to be deleted from the query string.
    book_id = request.args.get('id')
    # Find the Book object with that ID.
    book_to_delete = Book.query.get(book_id)
    # Delete the book from the database session and commit the changes.
    db.session.delete(book_to_delete)
    db.session.commit()
    # Redirect the user back to the home page.
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
