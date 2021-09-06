import os
from unittest import TestCase

from app import app
from models import connect_db


app.config["SQLALCHEMY_DATABASE_URI"] = (
    os.environ.get('DATABASE_URL', 'postgresql:///simply_art_test'))
app.config["SQLALCHEMY_ECHO"] = False
app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True

connect_db.drop_all()
connect_db.create_all()

##############################################################################
# Discover page (searchbar for users)


class SearchTestCase(TestCase):
    """Tests for searching api"""
    search_term = request.args.get('q')

    """Discover new artists(searchbar)."""
    url = "https://api.unsplash.com/search/collections?query={}&page=1&per_page=15&client_id=sjb8Hy9YhaHInjGNWAwQM9DMQdh4niqP7hiHnTlpGkU".format(
        search_term)

    res = requests.get(url)

    data = res.json()


##############################################################################
# About Page


@app.route('/about')
def about():
    """About Simply Art."""

    return render_template('about.html')

##############################################################################
# Artists page (page of all artists)


@app.route('/artists', methods=["GET", "POST"])
def artists():
    """Artists Bio page."""
    res = requests.get(
        'https://api.unsplash.com/photos/random?client_id=sjb8Hy9YhaHInjGNWAwQM9DMQdh4niqP7hiHnTlpGkU')

    data = res.json()

##############################################################################
# Homepage and error pages


@app.route('/')
def homepage():
    """Show homepage:
    """
    res = requests.get(
        'https://api.unsplash.com/photos/random?client_id=sjb8Hy9YhaHInjGNWAwQM9DMQdh4niqP7hiHnTlpGkU')

    data = res.json()


@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404
