"""End to End Tests."""

# import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .config import SeleniumTestBase

SERVICE_URL = "http://localhost:5000"
DRIVE_WAIT = 5


class TestSeleniumAuth(SeleniumTestBase):
    """This class contains the Selenium test cases for authentication."""

    def test_login(self):
        """Test logging in and logging out."""

        self.driver.get(f"{SERVICE_URL}/auth/auth?next=%2F")

        self.driver.find_element(
            By.XPATH, "//form[@id='signInFormLg']//input[@name='email']"
        ).send_keys("test@gmail.com")
        self.driver.find_element(
            By.XPATH, "//form[@id='signInFormLg']//input[@name='password']"
        ).send_keys("Password@123")
        self.std_wait.until(
            EC.element_to_be_clickable((By.ID, "signInSubmitLg"))
        ).click()

        WebDriverWait(self.driver, DRIVE_WAIT).until(EC.url_to_be(f"{SERVICE_URL}/"))
        self.assertEqual(self.driver.current_url, f"{SERVICE_URL}/")

    def test_logout(self):
        """Test logging out."""

        self.driver.get(f"{SERVICE_URL}/auth/logout")

        WebDriverWait(self.driver, DRIVE_WAIT).until(
            EC.url_to_be(f"{SERVICE_URL}/auth/auth")
        )
        self.assertEqual(self.driver.current_url, f"{SERVICE_URL}/auth/auth")


class TestEnd2End(SeleniumTestBase):
    """This class contains the end to end test cases."""

    def test_end_to_end(self):
        """Test the end to end flow of the application."""

        # login
        TestSeleniumAuth.test_login(self)

        # # click post on the home page
        # title_element = WebDriverWait(self.driver, DRIVE_WAIT).until(
        #     EC.visibility_of_element_located(
        #         (
        #             By.CSS_SELECTOR,
        #             "span.badge.rounded-pill.text-bg-primary.module-name.mb-3",
        #         )
        #     )
        # )
        # post_title = title_element.text

        # element = WebDriverWait(self.driver, DRIVE_WAIT).until(
        #     EC.element_to_be_clickable(
        #         (
        #             By.CSS_SELECTOR,
        #             "div.card.row-hover.pos-relative.pt-2.px-3.mb-3.\
        #                 border-primary.border-2.rounded-0",
        #         )
        #     )
        # )
        # onclick_attr = element.get_attribute("onclick")
        # url_match = re.search(r"window.open\('([^']*)'", onclick_attr)
        # self.assertEqual(url_match.group(1), f"{SERVICE_URL}/post/1")

        # logout
        TestSeleniumAuth.test_logout(self)
