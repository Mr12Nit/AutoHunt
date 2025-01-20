import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import logSetup


class WebDriverHandler:
    """
    A handler class for creating and managing Selenium WebDriver instances.
    """

    def __init__(self, driver_path: str, profile_path: str, logger=None):
        """
        Initializes the WebDriverHandler with paths and a logger.

        Args:
            driver_path (str): Path to the WebDriver executable.
            profile_path (str): Path to the Firefox profile directory.
            logger (optional): Custom logger instance. Defaults to a standard logger.
        """
        self.driver_path = driver_path
        self.profile_path = profile_path
        self.logger = logger or logSetup.log("WebDriverHandler", "webdriverLog.txt")

    def create_webdriver(self, headless: bool = False):
        """
        Creates and initializes a Selenium WebDriver instance.

        Args:
            headless (bool): Whether to run the browser in headless mode.

        Returns:
            WebDriver: The initialized WebDriver instance.

        Raises:
            FileNotFoundError: If the driver or profile path is invalid.
            RuntimeError: If the WebDriver initialization fails.
        """
        try:
            # Validate paths
            if not os.path.isfile(self.driver_path):
                self.logger.error(f"Driver path does not exist: {self.driver_path}")
                raise FileNotFoundError(f"Driver path does not exist: {self.driver_path}")

            if not os.path.isdir(self.profile_path):
                self.logger.error(f"Profile path does not exist: {self.profile_path}")
                raise FileNotFoundError(f"Profile path does not exist: {self.profile_path}")

            # Configure WebDriver options
            options = Options()
            if headless:
                options.add_argument("-headless")
            options.add_argument("--profile")
            options.add_argument(self.profile_path)

            # Initialize WebDriver
            driver = webdriver.Firefox(service=Service(self.driver_path), options=options)
            self.logger.info("WebDriver successfully created.")
            return driver
        except Exception as e:
            self.logger.error(f"Error creating WebDriver: {e}")
            raise RuntimeError(f"Failed to create WebDriver: {e}")

    def check_if_element_is_loaded(self, driver: webdriver.Firefox, element_class: str) -> bool:
        """
        Checks if a specific element is loaded on the page.

        Args:
            driver (WebDriver): The WebDriver instance to use.
            element_class (str): The class name of the element to check.

        Returns:
            bool: True if the element is loaded, False otherwise.
        """
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, element_class))
            )
            if element:
                self.logger.info(f"Element with class '{element_class}' is loaded.")
                return True
        except TimeoutException:
            self.logger.error(f"Timeout while waiting for element: {element_class}")
        except Exception as e:
            self.logger.error(f"Error checking element: {e}")
        return False
