import os

from flask import Flask, render_template, request, redirect, session, g, abort, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import connect_db, Message


import requests

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    os.environ.get('DATABASE_URL', 'postgresql:///simply_art_test'))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"]
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['WTF_CSRF_ENABLED'] = False
toolbar = DebugToolbarExtension(app)


connect_db(app)

##############################################################################
# Discover page (searchbar for users)


@app.route('/discover', methods=["GET", "POST"])
def discover():
    search_term = request.args.get('q')

    """Discover new artists(searchbar)."""
    url = "https://api.unsplash.com/search/collections?query={}&page=1&per_page=15&client_id=sjb8Hy9YhaHInjGNWAwQM9DMQdh4niqP7hiHnTlpGkU".format(
        search_term)

    res = requests.get(url)

    data = res.json()

    return render_template('discover.html', search_bar=data['results'][0]['preview_photos'][0]['urls']['regular'])

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

    return render_template('artists.html', background=data.get("user").get("profile_image").get("large"),
                           artist_name=data.get("user").get("name"), user_name=data.get("user").get("username"),
                           location=data.get("location").get("country"), bio=data.get("bio"),
                           portfolio=data.get("user").get("portfolio_url"), photos=data.get("user").get("links").get("photos"))

##############################################################################
# Homepage and error pages


@app.route('/')
def homepage():
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """
    res = requests.get(
        'https://api.unsplash.com/photos/random?client_id=sjb8Hy9YhaHInjGNWAwQM9DMQdh4niqP7hiHnTlpGkU')

    # res = json.loads(res.text)

    data = res.json()

    baseUrl = "https://www.unsplash.com"

    if g.user:
        following_ids = [f.id for f in g.user.following] + [g.user.id]

        messages = (Message
                    .query
                    .filter(Message.user_id.in_(following_ids))
                    .order_by(Message.timestamp.desc())
                    .limit(100)
                    .all())

        liked_msg_ids = [msg.id for msg in g.user.likes]

        return render_template('index.html', messages=messages, likes=liked_msg_ids, background=data.get("urls").get("full"))

    else:
        return render_template('index.html', background=data.get("urls").get("full"), artist_name=data.get("user").get("name"), baseUrl=baseUrl)


@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404
