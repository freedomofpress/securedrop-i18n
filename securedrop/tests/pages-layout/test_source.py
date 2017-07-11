import source
import journalist_navigation_steps
import source_navigation_steps
import functional_test
import pytest


@pytest.fixture
def tor2web(request):
    source.TEST_X_TOR2WEB = True

    def finalizer():
        source.TEST_X_TOR2WEB = False
    request.addfinalizer(finalizer)
    return None


class TestSourceLayout(
        functional_test.FunctionalTest,
        source_navigation_steps.SourceNavigationSteps,
        journalist_navigation_steps.JournalistNavigationSteps):

    def test_index_tor2web(self, tor2web):
        self._source_visits_source_homepage()
        self._screenshot('source-index_tor2web.png')

    def test_index(self):
        self._source_visits_source_homepage()
        self._screenshot('source-index.png')

    def test_index_javascript(self):
        self._javascript_toggle()
        self._source_visits_source_homepage()
        self._screenshot('source-index_javascript.png')

    def test_lookup(self):
        self._source_visits_source_homepage()
        self._source_chooses_to_submit_documents()
        self._source_continues_to_submit_page()
        self._source_submits_a_file()
        self._screenshot('source-lookup.png')

    def test_login(self):
        self._source_visits_source_homepage()
        self._source_chooses_to_login()
        self._screenshot('source-login.png')

    def test_use_tor_browser(self):
        self._source_visits_use_tor()
        self._screenshot('source-use_tor_browser.png')

    def test_generate(self):
        self._source_visits_source_homepage()
        self._source_chooses_to_submit_documents()
        self._screenshot('source-generate.png')

    def test_logout_flashed_message(self):
        self._source_visits_source_homepage()
        self._source_chooses_to_submit_documents()
        self._source_continues_to_submit_page()
        self._source_submits_a_file()
        self._source_logs_out()
        self._screenshot('source-logout_flashed_message.png')

    def test_next_submission_flashed_message(self):
        self._source_visits_source_homepage()
        self._source_chooses_to_submit_documents()
        self._source_continues_to_submit_page()
        self._source_submits_a_file()
        self._source_submits_a_message()
        self._screenshot('source-next_submission_flashed_message.png')

    def test_notfound(self):
        self._source_not_found()
        self._screenshot('source-notfound.png')

    def test_tor2web_warning(self):
        self._source_tor2web_warning()
        self._screenshot('source-tor2web_warning.png')

    def test_why_journalist_key(self):
        self._source_why_journalist_key()
        self._screenshot('source-why_journalist_key.png')
