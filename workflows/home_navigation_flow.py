from pages.home_page import HomePage

class HomeNavigationFlow:

    def __init__(self, executor):
        self.ex = executor

    def enter_intelligent_detection_and_back(self):
        self.ex.click_point(HomePage.MEDICAL_RECORD)
        self.ex.click_point("common.back")
