
from flask import Flask
from flask import request

##############################################################################


def test_base_route():
    app = Flask(__name__)
    client = app.test_client()
    url = "/"

    response = client.get(url)
    assert response.get_data()
    assert response.status_code == 200

    """Tests for searching api"""
    search_term = request.args.get('q')

    url = "https://api.unsplash.com/search/collections?query={}&page=1&per_page=15&client_id=sjb8Hy9YhaHInjGNWAwQM9DMQdh4niqP7hiHnTlpGkU".format(
        search_term)


def test_about_route():
    app = Flask(__name__)
    client = app.test_client()
    url = "/about"

    response = client.get(url)
    assert response.get_data()
    assert response.status_code == 200


def test_artists_route():
    app = Flask(__name__)
    client = app.test_client()
    url = "/artists"

    response = client.get(url)
    assert response.get_data()
    assert response.status_code == 200

    url = 'https://api.unsplash.com/photos/random?client_id=sjb8Hy9YhaHInjGNWAwQM9DMQdh4niqP7hiHnTlpGkU'
