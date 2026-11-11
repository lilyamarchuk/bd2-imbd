def post(c, url, data):
    return c.post(url, json=data)


def seed(c):
    g = post(c, "/api/genres", {"name": "Drama"}).get_json()["genre_id"]
    co = post(c, "/api/countries", {"name": "Ukraine", "code": "ua"}).get_json()["country_id"]
    m = post(c, "/api/movies", {"title": "Test Movie", "release_year": 2020}).get_json()["movie_id"]
    p = post(c, "/api/persons", {"full_name": "John Doe", "birth_date": "1980-05-01"}).get_json()["person_id"]
    r = post(c, "/api/roles", {"role_name": "Actor"}).get_json()["role_id"]
    return g, co, m, p, r


def test_crud_genre(client):
    r = post(client, "/api/genres", {"name": "Comedy"})
    assert r.status_code == 201
    gid = r.get_json()["genre_id"]
    assert client.get(f"/api/genres/{gid}").get_json()["name"] == "Comedy"
    assert client.put(f"/api/genres/{gid}", json={"name": "Dark Comedy"}).get_json()["name"] == "Dark Comedy"
    assert len(client.get("/api/genres").get_json()) == 1
    assert client.delete(f"/api/genres/{gid}").status_code == 200
    assert client.get(f"/api/genres/{gid}").status_code == 404


def test_validation_errors(client):
    assert post(client, "/api/movies", {"release_year": 2000}).status_code == 400
    assert post(client, "/api/movies", {"title": "X", "release_year": 1500}).status_code == 400
    assert post(client, "/api/countries", {"name": "X", "code": "USA"}).status_code == 400
    assert client.post("/api/genres", data="not json", content_type="application/json").status_code == 400


def test_country_code_uppercased_and_unique(client):
    seed(client)
    assert client.get("/api/countries/1").get_json()["code"] == "UA"
    assert post(client, "/api/countries", {"name": "Other", "code": "UA"}).status_code == 409


def test_many_to_many_movie_genres(client):
    g, co, m, p, r = seed(client)
    assert client.post(f"/api/movies/{m}/genres/{g}").status_code == 201
    assert [x["name"] for x in client.get(f"/api/movies/{m}/genres").get_json()] == ["Drama"]
    assert [x["title"] for x in client.get(f"/api/genres/{g}/movies").get_json()] == ["Test Movie"]
    assert client.delete(f"/api/movies/{m}/genres/{g}").status_code == 200
    assert client.get(f"/api/genres/{g}/movies").get_json() == []
    assert client.post(f"/api/movies/{m}/genres/999").status_code == 404


def test_many_to_many_movie_countries(client):
    g, co, m, p, r = seed(client)
    client.post(f"/api/movies/{m}/countries/{co}")
    assert client.get(f"/api/countries/{co}/movies").get_json()[0]["movie_id"] == m


def test_many_to_one_cast_and_filmography(client):
    g, co, m, p, r = seed(client)
    res = post(client, "/api/cast", {"movie_id": m, "person_id": p, "role_id": r, "character_name": "Hero"})
    assert res.status_code == 201
    assert client.get(f"/api/movies/{m}/cast").get_json()[0]["person_name"] == "John Doe"
    assert client.get(f"/api/persons/{p}/filmography").get_json()[0]["movie_title"] == "Test Movie"
    assert client.get(f"/api/roles/{r}/cast").get_json()[0]["role_name"] == "Actor"
    assert post(client, "/api/cast", {"movie_id": 999, "person_id": p, "role_id": r}).status_code == 400


def test_role_delete_restricted_and_cascade(client):
    g, co, m, p, r = seed(client)
    post(client, "/api/cast", {"movie_id": m, "person_id": p, "role_id": r})
    assert client.delete(f"/api/roles/{r}").status_code == 409
    assert client.delete(f"/api/movies/{m}").status_code == 200
    assert client.get("/api/cast").get_json() == []


def test_ratings_rules_and_average(client):
    g, co, m, p, r = seed(client)
    assert post(client, "/api/ratings", {"movie_id": m, "user_name": "a", "score": 8}).status_code == 201
    assert post(client, "/api/ratings", {"movie_id": m, "user_name": "a", "score": 9}).status_code == 409
    assert post(client, "/api/ratings", {"movie_id": m, "user_name": "b", "score": 11}).status_code == 400
    post(client, "/api/ratings", {"movie_id": m, "user_name": "c", "score": 9})
    assert client.get(f"/api/ratings/movie/{m}/average").get_json()["average_rating"] == 8.5
    assert client.get("/api/movies/top?limit=1").get_json()[0]["movie_id"] == m


def test_movie_details_and_search(client):
    g, co, m, p, r = seed(client)
    client.post(f"/api/movies/{m}/genres/{g}")
    post(client, "/api/box-office", {"movie_id": m, "country_id": co, "amount_usd": 1000})
    d = client.get(f"/api/movies/{m}/details").get_json()
    assert d["genres"] == ["Drama"] and d["box_office_total_usd"] == 1000.0
    assert len(client.get("/api/movies?title=Test").get_json()) == 1
    assert client.get("/api/movies?year=1999").get_json() == []


def test_reviews_date_filter(client):
    g, co, m, p, r = seed(client)
    post(client, "/api/reviews", {"movie_id": m, "author_name": "A", "review_text": "ok", "review_date": "2023-05-01"})
    assert len(client.get("/api/reviews?from=2023-01-01&to=2023-12-31").get_json()) == 1
    assert client.get("/api/reviews?from=2024-01-01&to=2024-12-31").get_json() == []
    assert post(client, "/api/reviews", {"movie_id": m, "author_name": "A", "review_text": "x", "review_date": "bad"}).status_code == 400
