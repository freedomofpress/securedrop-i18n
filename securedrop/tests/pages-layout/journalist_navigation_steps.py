from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import crypto_util
import tests.utils.db_helper as db_helper

import db

from tests.functional import journalist_navigation_steps


class JournalistNavigationSteps(
        journalist_navigation_steps.JournalistNavigationSteps):

    def _visit_edit_account(self):
        edit_account_link = self.driver.find_element_by_id(
            'link_edit_account')
        edit_account_link.click()

    def _visit_edit_hotp_secret(self):
        hotp_reset_button = self.driver.find_elements_by_css_selector(
            '#reset-two-factor-hotp')[0]
        assert ('/account/reset-2fa-hotp' in
                hotp_reset_button.get_attribute('action'))

        hotp_reset_button.click()

    def _set_hotp_secret(self):
        hotp_secret_field = self.driver.find_elements_by_css_selector(
            'input[name="otp_secret"]')[0]
        hotp_secret_field.send_keys('123456')
        submit_button = self.driver.find_element_by_css_selector(
            'button[type=submit]')
        submit_button.click()

    def _visit_edit_totp_secret(self):
        totp_reset_button = self.driver.find_elements_by_css_selector(
            '#reset-two-factor-totp')[0]
        assert ('/account/reset-2fa-totp' in
                totp_reset_button.get_attribute('action'))
        totp_reset_button.click()

    def _admin_visits_add_user(self):
        add_user_btn = self.driver.find_element_by_css_selector(
            'button#add-user')
        add_user_btn.click()

    def _admin_visits_edit_user(self):
        new_user_edit_links = filter(
            lambda el: (el.get_attribute('data-username') ==
                        self.new_user['username']),
            self.driver.find_elements_by_tag_name('a'))
        assert len(new_user_edit_links) == 1
        new_user_edit_links[0].click()

        def can_edit_user():
            assert ('"{}"'.format(self.new_user['username']) in
                    self.driver.page_source)
        self.wait_for(can_edit_user)

    def _admin_visits_reset_2fa_hotp(self):
        hotp_reset_button = self.driver.find_elements_by_css_selector(
            '#reset-two-factor-hotp')[0]
        assert ('/admin/reset-2fa-hotp' in
                hotp_reset_button.get_attribute('action'))
        hotp_reset_button.click()

    def _admin_visits_reset_2fa_totp(self):
        totp_reset_button = self.driver.find_elements_by_css_selector(
            '#reset-two-factor-totp')[0]
        assert ('/admin/reset-2fa-totp' in
                totp_reset_button.get_attribute('action'))
        totp_reset_button.click()

    def _admin_creates_a_user(self, hotp):
        add_user_btn = self.driver.find_element_by_css_selector(
            'button#add-user')
        add_user_btn.click()

        self.new_user = dict(
            username='dellsberg',
            password='pentagonpapers')

        self._add_user(self.new_user['username'],
                       self.new_user['password'],
                       is_admin=False,
                       hotp=hotp)

    def _journalist_visits_col(self):
        self.driver.find_element_by_css_selector(
            '#un-starred-source-link-1').click()

    def _journalist_delete_all(self):
        for checkbox in self.driver.find_elements_by_name(
                'doc_names_selected'):
            checkbox.click()
        self.driver.find_element_by_id('delete_selected').click()

    def _journalist_confirm_delete_all(self):
        self.wait_for(
            lambda: self.driver.find_element_by_id('confirm_delete'))
        confirm_btn = self.driver.find_element_by_id('confirm_delete')
        confirm_btn.click()

    def _source_delete_key(self):
        filesystem_id = crypto_util.hash_codename(self.source_name)
        crypto_util.delete_reply_keypair(filesystem_id)

    def _journalist_continues_after_flagging(self):
        self.driver.find_element_by_id('continue-to-list').click()

    def _journalist_delete_none(self):
        self.driver.find_element_by_id('delete_selected').click()

    def _journalist_delete_one_javascript(self):
        self.driver.find_elements_by_name('doc_names_selected')[0].click()
        self.driver.find_element_by_id('delete_selected').click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.alert_is_present(),
            'Timed out waiting confirmation popup to appear.')

    def _accept(self):
        self.driver.switch_to.alert.accept()

    def _journalist_delete_all_javascript(self):
        self.driver.find_element_by_id('select_all').click()
        self.driver.find_element_by_id('delete_selected').click()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.alert_is_present(),
            'Timed out waiting confirmation popup to appear.')

    def _journalist_delete_one(self):
        self.driver.find_elements_by_name('doc_names_selected')[0].click()
        self.driver.find_element_by_id('delete_selected').click()

    def _journalist_flags_source(self):
        self.driver.find_element_by_id('flag-button').click()

    def _journalist_visits_admin(self):
        self.driver.get(self.journalist_location + "/admin")

    def _journalist_fail_login(self):
        self.user, self.user_pw = db_helper.init_journalist()
        self._try_login_user(self.user.username, 'worse', 'mocked')

    def _journalist_fail_login_many(self):
        self.user, self.user_pw = db_helper.init_journalist()
        for _ in range(db.Journalist._MAX_LOGIN_ATTEMPTS_PER_PERIOD + 1):
            self._try_login_user(self.user.username, 'worse', 'mocked')
