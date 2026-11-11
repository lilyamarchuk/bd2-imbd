from my_project.utils.db import db
from my_project.auth.domain.base import BaseModel


movie_genres = db.Table(
    "movie_genres",
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.movie_id", ondelete="CASCADE"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.genre_id", ondelete="CASCADE"), primary_key=True),
)

movie_countries = db.Table(
    "movie_countries",
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.movie_id", ondelete="CASCADE"), primary_key=True),
    db.Column("country_id", db.Integer, db.ForeignKey("countries.country_id", ondelete="CASCADE"), primary_key=True),
)

CASCADE = dict(cascade="all, delete-orphan", passive_deletes=True)


class Genre(BaseModel):
    __tablename__ = "genres"
    __writable__ = ("name",)
    genre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class Country(BaseModel):
    __tablename__ = "countries"
    __writable__ = ("name", "code")
    country_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code = db.Column(db.String(2), nullable=False, unique=True)


class Person(BaseModel):
    __tablename__ = "persons"
    __writable__ = ("full_name", "birth_date", "birth_place", "biography")
    person_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(150), nullable=False)
    birth_date = db.Column(db.Date)
    birth_place = db.Column(db.String(150))
    biography = db.Column(db.Text)


class Role(BaseModel):
    __tablename__ = "roles"
    __writable__ = ("role_name",)
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(50), nullable=False, unique=True)


class Movie(BaseModel):
    __tablename__ = "movies"
    __writable__ = ("title", "original_title", "release_year", "duration_min", "description", "age_rating")
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    original_title = db.Column(db.String(255))
    release_year = db.Column(db.Integer, nullable=False)
    duration_min = db.Column(db.Integer)
    description = db.Column(db.Text)
    age_rating = db.Column(db.String(10))

    genres = db.relationship("Genre", secondary=movie_genres, backref=db.backref("movies", lazy="select"),
                             order_by="Genre.name")
    countries = db.relationship("Country", secondary=movie_countries, backref=db.backref("movies", lazy="select"),
                                order_by="Country.name")


class MovieCast(BaseModel):
    __tablename__ = "movie_cast"
    __writable__ = ("movie_id", "person_id", "role_id", "character_name")
    cast_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id", ondelete="CASCADE"), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.person_id", ondelete="CASCADE"), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.role_id", ondelete="RESTRICT"), nullable=False)
    character_name = db.Column(db.String(150))

    movie = db.relationship("Movie", backref=db.backref("cast", **CASCADE))
    person = db.relationship("Person", backref=db.backref("filmography", **CASCADE))
    role = db.relationship("Role", backref=db.backref("cast", passive_deletes="all"))

    def to_dto(self):
        dto = super().to_dto()
        dto["movie_title"] = self.movie.title if self.movie else None
        dto["person_name"] = self.person.full_name if self.person else None
        dto["role_name"] = self.role.role_name if self.role else None
        return dto


class Review(BaseModel):
    __tablename__ = "reviews"
    __writable__ = ("movie_id", "author_name", "review_text", "review_date")
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id", ondelete="CASCADE"), nullable=False)
    author_name = db.Column(db.String(100), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    review_date = db.Column(db.Date, nullable=False)

    movie = db.relationship("Movie", backref=db.backref("reviews", **CASCADE))


class Rating(BaseModel):
    __tablename__ = "ratings"
    __writable__ = ("movie_id", "user_name", "score", "rating_date")
    __table_args__ = (db.UniqueConstraint("movie_id", "user_name", name="uk_rating_user_movie"),)
    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id", ondelete="CASCADE"), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Numeric(3, 1), nullable=False)
    rating_date = db.Column(db.Date, nullable=False)

    movie = db.relationship("Movie", backref=db.backref("ratings", **CASCADE))


class Trivia(BaseModel):
    __tablename__ = "trivia"
    __writable__ = ("movie_id", "fact_text")
    trivia_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id", ondelete="CASCADE"), nullable=False)
    fact_text = db.Column(db.Text, nullable=False)

    movie = db.relationship("Movie", backref=db.backref("trivia", **CASCADE))


class BoxOffice(BaseModel):
    __tablename__ = "box_office"
    __writable__ = ("movie_id", "country_id", "amount_usd")
    __table_args__ = (db.UniqueConstraint("movie_id", "country_id", name="uk_movie_country"),)
    box_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id", ondelete="CASCADE"), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey("countries.country_id", ondelete="CASCADE"), nullable=False)
    amount_usd = db.Column(db.Numeric(15, 2), nullable=False)

    movie = db.relationship("Movie", backref=db.backref("box_office", **CASCADE))
    country = db.relationship("Country", backref=db.backref("box_office", **CASCADE))

    def to_dto(self):
        dto = super().to_dto()
        dto["movie_title"] = self.movie.title if self.movie else None
        dto["country_name"] = self.country.name if self.country else None
        return dto
