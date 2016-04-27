import base64
import os
import urllib

import flask

import requests


OAUTH_CLIENT_ID = "geekieid-connect-example-python"

app = flask.Flask(__name__)
app.secret_key = os.urandom(32)
app.config["PROPAGATE_EXCEPTIONS"] = True


@app.route("/")
def home():
    if "access_token" in flask.session:
        response = requests.get(
            "https://core.api.geekielab.com.br/public/auth/me",
            headers={"Authorization": "Bearer " + flask.session["access_token"]},
        )
        if response.status_code != 200:
            del flask.session["access_token"]
            return oauth_fail("User info request failed", response.content)

        user_data = response.json()

        full_name = user_data.get("_embedded", {}).get("membership", {}).get("full_name")
        email = user_data.get("_embedded", {}).get("membership", {}).get("email")

        return flask.render_template(
            "home.html",
            status="logged in",
            full_name=full_name,
            email=email,
        )

    else:
        return flask.render_template(
            "home.html",
            status="anonymous",
        )


@app.route("/login-with-geekie")
def launch_login_with_geekie():
    csrf_state = base64.b32encode(os.urandom(32))
    flask.session["csrf_state"] = csrf_state

    print "csrf_state", repr(csrf_state)

    url_params = {
        "response_type": "code",
        "client_id": OAUTH_CLIENT_ID,
        "state": csrf_state,
    }

    return flask.redirect(
        "https://core.api.geekielab.com.br/public/authorize?" + urllib.urlencode(url_params))


@app.route("/oauthcallback")
def oauth_callback():
    # First of call, to prevent CSRF attacks, we verify if the state is
    # the same one we previously sent.
    print "in session:", repr(flask.session.get("csrf_state"))
    print "in qs     :", repr(flask.request.args.get("state"))
    if flask.session.get("csrf_state") != flask.request.args.get("state"):
        return "Invalid CSRF state.", 400

    # Now we follow two different paths depending on whether or not the
    # OAuth authorization was successful
    if "code" in flask.request.args:
        response = requests.post(
            "https://core.api.geekielab.com.br/public/auth/access-tokens",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "authorization_code",
                "client_id": OAUTH_CLIENT_ID,
                "code": flask.request.args["code"],
            },
        )
        if response.status_code != 200:
            return oauth_fail("Failed while obtaining an access token", response.content)

        print "Access Token Response:"
        print response.content

        flask.session["access_token"] = response.json()["access_token"]

        return flask.redirect(flask.url_for("home"))

    elif "error" in flask.request.args:
        return oauth_fail("Authorization failed", flask.request.args["error"])

    else:
        return oauth_fail("Invalid request")


def oauth_fail(msg, detail=None):
    print "{}{}{}".format(msg, ": " if detail else "", detail or "")
    return "{}.".format(msg), 400
