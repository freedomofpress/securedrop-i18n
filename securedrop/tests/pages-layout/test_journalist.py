from tests.functional import functional_test, journalist_navigation_steps
import os
from os.path import abspath, dirname, realpath
import unittest

LOG_DIR = abspath(os.path.join(dirname(realpath(__file__)), 'screenshots'))

class JouranlistLayoutTest(
        unittest.TestCase,
        functional_test.FunctionalTest,
        journalist_navigation_steps.JournalistNavigationSteps):

    def setUp(self):
        functional_test.FunctionalTest.setUp(self)

    def tearDown(self):
        functional_test.FunctionalTest.tearDown(self)

    def _visit_edit_account(self):
        edit_account_link = self.driver.find_element_by_link_text(
            'Edit Account')
        edit_account_link.click()

    def _visit_edit_hotp_secret(self):
        hotp_reset_button = self.driver.find_elements_by_css_selector(
            '#reset-two-factor-hotp')[0]
        self.assertRegexpMatches(hotp_reset_button.get_attribute('action'),
                                 '/account/reset-2fa-hotp')
        hotp_reset_button.click()

    def test_account_edit_hotp_secret(self):
        self._journalist_logs_in()
        self._visit_edit_account()
        self._visit_edit_hotp_secret()
        self.driver.save_screenshot(os.path.join(LOG_DIR, 'journalist-account_edit_hotp_secret.png'))

    def _set_hotp_secret(self):
        hotp_secret_field = self.driver.find_elements_by_css_selector(
            'input[name="otp_secret"]')[0]
        hotp_secret_field.send_keys('123456')
        submit_button = self.driver.find_element_by_css_selector(
            'button[type=submit]')
        submit_button.click()

    def test_account_new_two_factor_hotp(self):
        self._journalist_logs_in()
        self._visit_edit_account()
        self._visit_edit_hotp_secret()
        self._set_hotp_secret()
        self.driver.save_screenshot(os.path.join(LOG_DIR, 'journalist-account_new_two_factor_hotp.png'))

    def _visit_edit_totp_secret(self):
        totp_reset_button = self.driver.find_elements_by_css_selector(
            '#reset-two-factor-totp')[0]
        self.assertRegexpMatches(totp_reset_button.get_attribute('action'),
                                 '/account/reset-2fa-totp')
        totp_reset_button.click()
    
    def test_account_new_two_factor_totp(self):
        self._journalist_logs_in()
        self._visit_edit_account()
        self._visit_edit_totp_secret()
        self.driver.save_screenshot(os.path.join(LOG_DIR, 'journalist-account_new_two_factor_totp.png'))

    def _admin_visits_add_user(self):
        add_user_btn = self.driver.find_element_by_css_selector(
            'button#add-user')
        add_user_btn.click()
        
    def test_admin_add_user(self):
        self._admin_logs_in()
        self._admin_visits_admin_interface()
        self._admin_visits_add_user()
        self.driver.save_screenshot(os.path.join(LOG_DIR, 'journalist-admin_add_user.png'))

    def _admin_visits_edit_user(self):
        new_user_edit_links = filter(
            lambda el: el.get_attribute('data-username') == self.new_user['username'],
            self.driver.find_elements_by_tag_name('a'))
        self.assertEquals(len(new_user_edit_links), 1)
        new_user_edit_links[0].click()
        self.wait_for(
            lambda: self.assertIn('Edit user "{}"'.format(
                self.new_user['username']),
                self.driver.page_source)
        )

    def _admin_visits_reset_2fa_hotp(self):
        hotp_reset_button = self.driver.find_elements_by_css_selector(
            '#reset-two-factor-hotp')[0]
        self.assertRegexpMatches(hotp_reset_button.get_attribute('action'),
                                 '/admin/reset-2fa-hotp')
        hotp_reset_button.click()
    
    def test_admin_edit_hotp_secret(self):
        self._admin_logs_in()
        self._admin_visits_admin_interface()
        self._admin_adds_a_user()
        self._admin_visits_edit_user()
        self._admin_visits_reset_2fa_hotp()
        self.driver.save_screenshot(os.path.join(LOG_DIR, 'journalist-admin_edit_hotp_secret.png'))

    def _admin_visits_reset_2fa_totp(self):
        totp_reset_button = self.driver.find_elements_by_css_selector(
            '#reset-two-factor-totp')[0]
        self.assertRegexpMatches(totp_reset_button.get_attribute('action'),
                                 '/admin/reset-2fa-totp')
        totp_reset_button.click()
    
    def test_admin_edit_totp_secret(self):
        self._admin_logs_in()
        self._admin_visits_admin_interface()
        self._admin_adds_a_user()
        self._admin_visits_edit_user()
        self._admin_visits_reset_2fa_totp()
        self.driver.save_screenshot(os.path.join(LOG_DIR, 'journalist-admin_edit_totp_secret.png'))

    def test_login(self):
        self.driver.get(self.journalist_location + "/login")
        self.driver.save_screenshot(os.path.join(LOG_DIR, 'journalist-login.png'))

    def test_admin(self):
        self._admin_logs_in()
        self.driver.save_screenshot(os.path.join(LOG_DIR, 'journalist-admin.png'))

    def _admin_creates_a_user(self, hotp):
        add_user_btn = self.driver.find_element_by_css_selector(
            'button#add-user')
        add_user_btn.click()

        # The add user page has a form with an "ADD USER" button
        btns = self.driver.find_elements_by_tag_name('button')
        self.assertIn('ADD USER', [el.text for el in btns])

        self.new_user = dict(
            username='dellsberg',
            password='pentagonpapers')

        self._add_user(self.new_user['username'],
                       self.new_user['password'],
                       is_admin=False,
                       hotp=hotp)
        
    def test_admin_new_user_two_factor_hotp(self):
        self._admin_logs_in()
        self._admin_visits_admin_interface()
        self._admin_creates_a_user(hotp='123456')
        self.driver.save_screenshot(os.path.join(LOG_DIR, 'journalist-admin_new_user_two_factor_hotp.png'))

    def test_admin_new_user_two_factor_totp(self):
        self._admin_logs_in()
        self._admin_visits_admin_interface()
        self._admin_creates_a_user(hotp=None)
        self.driver.save_screenshot(os.path.join(LOG_DIR, 'journalist-admin_new_user_two_factor_totp.png'))
