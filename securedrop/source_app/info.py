# -*- coding: utf-8 -*-
import flask
from flask import Blueprint, render_template, send_file, redirect, url_for
import werkzeug

from io import BytesIO  # noqa

from encryption import EncryptionManager
from sdconfig import SDConfig


def make_blueprint(config: SDConfig) -> Blueprint:
    view = Blueprint('info', __name__)

    @view.route('/tor2web-warning')
    def tor2web_warning() -> str:
        return render_template("tor2web-warning.html")

    @view.route('/use-tor')
    def recommend_tor_browser() -> str:
        return render_template("use-tor-browser.html")

    @view.route('/public-key')
    def download_public_key() -> flask.Response:
        journalist_pubkey = EncryptionManager.get_default().get_journalist_public_key()
        data = BytesIO(journalist_pubkey.encode('utf-8'))
        return send_file(data,
                         mimetype="application/pgp-keys",
                         attachment_filename=config.JOURNALIST_KEY + ".asc",
                         as_attachment=True)

    @view.route('/journalist-key')
    def download_journalist_key() -> werkzeug.wrappers.Response:
        return redirect(url_for('.download_public_key'), code=301)

    @view.route('/why-public-key')
    def why_download_public_key() -> str:
        return render_template("why-public-key.html")

    return view
