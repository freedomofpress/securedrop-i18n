from tests.functional import source_navigation_steps


class SourceNavigationSteps(source_navigation_steps.SourceNavigationSteps):

    def _source_visits_use_tor(self):
        self.driver.get(self.source_location + "/use-tor")

    def _source_not_found(self):
        self.driver.get(self.source_location + "/unknown")

    def _source_tor2web_warning(self):
        self.driver.get(self.source_location + "/tor2web-warning")

    def _source_why_journalist_key(self):
        self.driver.get(self.source_location + "/why-journalist-key")
