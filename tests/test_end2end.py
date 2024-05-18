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

    def login(self, email: str = "test@gmail.com", password: str = "Password@123"):
        """Test logging in and logging out."""

        self.driver.get(f"{SERVICE_URL}/auth/auth?next=%2F")

        self.driver.find_element(
            By.XPATH, "//form[@id='signInFormLg']//input[@name='email']"
        ).send_keys(email)
        self.driver.find_element(
            By.XPATH, "//form[@id='signInFormLg']//input[@name='password']"
        ).send_keys(password)
        self.std_wait.until(
            EC.element_to_be_clickable((By.ID, "signInSubmitLg"))
        ).click()

        WebDriverWait(self.driver, DRIVE_WAIT).until(EC.url_to_be(f"{SERVICE_URL}/"))
        self.assertEqual(self.driver.current_url, f"{SERVICE_URL}/")

    def logout(self):
        """Test logging out."""

        self.driver.get(f"{SERVICE_URL}/auth/auth?next=%2F")

        WebDriverWait(self.driver, DRIVE_WAIT).until(
            EC.url_to_be(f"{SERVICE_URL}/auth/auth")
        )
        self.assertEqual(self.driver.current_url, f"{SERVICE_URL}/auth/auth")


class TestEnd2End(SeleniumTestBase):
    """This class contains the end to end test cases."""

    def test_register(self):
        """Test the registration flow of the application."""

        self.driver.get(f"{SERVICE_URL}/auth/auth")

        self.driver.find_element(
            By.XPATH, "//form[@id='signUpFormLg']//input[@name='username']"
        ).send_keys("end2endTest")
        self.driver.find_element(
            By.XPATH, "//form[@id='signUpFormLg']//input[@name='email']"
        ).send_keys("end2endTest@gmail.com")
        self.driver.find_element(
            By.XPATH, "//form[@id='signUpFormLg']//input[@name='password']"
        ).send_keys("Password@123")
        self.driver.find_element(
            By.XPATH, "//form[@id='signUpFormLg']//input[@name='rpassword']"
        ).send_keys("Password@123")
        self.driver.find_element(
            By.XPATH, "//form[@id='signUpFormLg']//input[@name='squestion']"
        ).send_keys("What is your favorite color?")
        self.driver.find_element(
            By.XPATH, "//form[@id='signUpFormLg']//input[@name='sanswer']"
        ).send_keys("blue")
        element = self.driver.find_element(By.ID, "signUpSubmitLg")
        self.driver.execute_script("arguments[0].click();", element)

        WebDriverWait(self.driver, DRIVE_WAIT).until(
            EC.url_to_be(f"{SERVICE_URL}/auth/auth")
        )
        self.assertEqual(self.driver.current_url, f"{SERVICE_URL}/auth/auth")

    def test_update_profile(self):
        """Test updating the profile of the user."""

        # login
        TestSeleniumAuth.login(self)

        # update profile
        self.driver.get(f"{SERVICE_URL}/users/profile")

        self.driver.find_element(
            By.XPATH, "//form[@id='profileForm']//input[@name='username']"
        ).send_keys("test123")
        self.driver.find_element(
            By.XPATH, "//form[@id='profileForm']//input[@name='email']"
        ).send_keys("test123@gmail.com")
        element = self.driver.find_element(By.ID, "profileSubmit")
        self.driver.execute_script("arguments[0].click();", element)

    def test_add_community(self):
        """Test adding a community."""

        # login
        TestSeleniumAuth.login(self)

        # add community
        self.driver.get(f"{SERVICE_URL}/communities/management")

        self.driver.find_element(
            By.XPATH, "//form[@id='communityForm']//input[@name='name']"
        ).send_keys("test")
        self.driver.find_element(
            By.XPATH, "//form[@id='communityForm']//textarea[@name='description']"
        ).send_keys("test description")
        element = self.driver.find_element(By.ID, "communitySubmit")
        self.driver.execute_script("arguments[0].click();", element)

    def test_edit_community(self):
        """Test editing a community."""

        # login
        TestSeleniumAuth.login(self)

        # edit community
        self.driver.get(f"{SERVICE_URL}/communities/management/1")

        self.driver.find_element(
            By.XPATH, "//form[@id='communityForm']//input[@name='name']"
        ).send_keys("test_edit")
        element = self.driver.find_element(By.ID, "communitySubmit")
        self.driver.execute_script("arguments[0].click();", element)
