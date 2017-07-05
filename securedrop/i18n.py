#
# SecureDrop whistleblower submission system
# Copyright (C) 2017 Loic Dachary <loic@dachary.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from flask import request
from flask_babel import Babel

import config
import os

LOCALES = set()
babel = None


def setup_app(app):
    global babel
    babel = Babel(app)
    assert 1 == len(list(babel.translation_directories))
    for filename in os.listdir(next(babel.translation_directories)):
        if '_' in filename:
            LOCALES.add(filename)

    babel.localeselector(get_locale)


def get_locale():
    """
    Get the locale as follows, by order of precedence:
    - browser suggested locale, according to best_match
    - config.LOCALE
    - en_US
    """
    locale = request.accept_languages.best_match(LOCALES)
    if locale in LOCALES:
        return locale
    else:
        return getattr(config, 'LOCALE', 'en_US')
