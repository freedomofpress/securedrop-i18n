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
import argparse
import logging
import os

from flask import request, render_template_string
from flask_babel import gettext
from werkzeug.datastructures import Headers

os.environ['SECUREDROP_ENV'] = 'test'  # noqa
import config
import i18n
import journalist
import manage
import source


class TestI18N(object):

    def verify_i18n(self, app):
        not_translated = 'code hello i18n'
        translated = 'code bonjour'

        for accepted in ('unknown', 'en_US'):
            headers = Headers([('Accept-Language', accepted)])
            with app.test_request_context(headers=headers):
                assert not hasattr(request, 'babel_locale')
                assert not_translated == gettext(not_translated)
                assert hasattr(request, 'babel_locale')
                assert render_template_string('''
                {{ gettext('code hello i18n') }}
                ''').strip() == not_translated

        headers = Headers([('Accept-Language', 'fr_FR')])
        with app.test_request_context(headers=headers):
            assert not hasattr(request, 'babel_locale')
            assert translated == gettext(not_translated)
            assert hasattr(request, 'babel_locale')
            assert render_template_string('''
            {{ gettext('code hello i18n') }}
            ''').strip() == translated

    def test_i18n(self):
        sources = [
            'tests/i18n/code.py',
            'tests/i18n/template.html',
        ]
        kwargs = {
            'translations_dir': config.TEMP_DIR,
            'mapping': 'tests/i18n/babel.cfg',
            'source': sources,
            'extract_update': True,
            'compile': True,
            'verbose': logging.DEBUG,
        }
        args = argparse.Namespace(**kwargs)
        manage.setup_verbosity(args)
        manage.translate(args)

        manage.sh("""
        pybabel init -i {d}/messages.pot -d {d} -l en_US
        pybabel init -i {d}/messages.pot -d {d} -l fr_FR
        sed -i -e '/code hello i18n/,+1s/msgstr ""/msgstr "code bonjour"/' \
              {d}/fr_FR/LC_MESSAGES/messages.po
        """.format(d=config.TEMP_DIR))

        manage.translate(args)
        os.system("cat /tmp/securedrop/tmp/fr_FR/LC_MESSAGES/messages.po")

        for app in (journalist.app, source.app):
            app.config['BABEL_TRANSLATION_DIRECTORIES'] = config.TEMP_DIR
            i18n.setup_app(app)
            self.verify_i18n(app)

    @classmethod
    def tearDownClass(cls):
        # Reset the module variables that were changed to mocks so we don't
        # break other tests
        reload(journalist)
        reload(source)
        reload(config)
        reload(i18n)
