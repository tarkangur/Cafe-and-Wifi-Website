from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, URL
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def cafes_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class CafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    map_url = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    img_url = StringField('Cafe Image (URL)', validators=[DataRequired(), URL()])
    location = StringField('Location', validators=[DataRequired()])
    has_sockets = SelectField("Sockets", validators=[DataRequired()], choices=[("Yes", "Yes"), ("No", "No")])
    has_toilet = SelectField("Toilets", validators=[DataRequired()], choices=[("Yes", "Yes"), ("No", "No")])
    has_wifi = SelectField("WiFi", validators=[DataRequired()], choices=[("Yes", "Yes"), ("No", "No")])
    can_take_calls = SelectField("Can take Calls", validators=[DataRequired()], choices=[("Yes", "Yes"), ("No", "No")])
    seats = IntegerField("Seats", validators=[DataRequired()])
    coffee_price = StringField("Coffee Price", validators=[DataRequired()])
    submit = SubmitField("Submit")


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cafes")
def all_cafes():
    cafes = Cafe.query.all()
    return render_template("cafes.html", cafes=cafes)


@app.route("/add_cafe", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data == "Yes",
            has_toilet=form.has_toilet.data == "Yes",
            has_wifi=form.has_wifi.data == "Yes",
            can_take_calls=form.can_take_calls.data == "Yes",
            seats=form.seats.data,
            coffee_price=form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("all_cafes"))
    return render_template("add_cafe.html", form=form)


@app.route("/delete/<int:cafe_id>", methods=["DELETE", "GET"])
def delete_cafe(cafe_id):
    cafe = db.get_or_404(Cafe, cafe_id)
    if cafe:
        db.session.delete(cafe)
        db.session.commit()
        return redirect(url_for("all_cafes"))


if __name__ == '__main__':
    app.run(debug=True)
