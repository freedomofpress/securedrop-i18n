from datetime import datetime
import os
from os.path import abspath, dirname, realpath
import pytest

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from selenium.webdriver.firefox import firefox_binary

from tests.functional import functional_test


def list_locales():
    d = os.path.join(dirname(__file__), '..', '..', 'translations')
    files = os.listdir(d)
    return ['en_US'] + [f for f in files if '_' in f]


class FunctionalTest(functional_test.FunctionalTest):

    @pytest.fixture(autouse=True, params=list_locales())
    def webdriver_fixture(self, request):
        self.accept_languages = request.param
        self.log_dir = abspath(
            os.path.join(dirname(realpath(__file__)),
                         'screenshots', self.accept_languages))
        os.system("mkdir -p " + self.log_dir)
        log_file = open(os.path.join(self.log_dir, 'firefox.log'), 'a')
        log_file.write(
            '\n\n[%s] Running Functional Tests\n' % str(
                datetime.now()))
        log_file.flush()
        firefox = firefox_binary.FirefoxBinary(log_file=log_file)
        profile = webdriver.FirefoxProfile()
        profile.set_preference("intl.accept_languages", self.accept_languages)
        self.override_driver = True
        self.driver = webdriver.Firefox(firefox_binary=firefox,
                                        firefox_profile=profile)
        self._javascript_toggle()

        yield None

        self.driver.quit()

    def _javascript_toggle(self):
        # the following is a noop for some reason, workaround it
        # profile.set_preference("javascript.enabled", False)
        # https://stackoverflow.com/a/36782979/837471
        self.driver.get("about:config")
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.RETURN)
        actions.send_keys("javascript.enabled")
        actions.perform()
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.RETURN)
        actions.send_keys(Keys.F5)
        actions.perform()

    def _screenshot(self, filename):
        self.driver.save_screenshot(os.path.join(self.log_dir, filename))

    def _save_alert(self, filename):
        fd = open(os.path.join(self.log_dir, filename), 'wb')
        fd.write(self.driver.switch_to.alert.text.encode('utf-8'))
        fd.close()
