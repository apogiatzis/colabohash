import time
import re
import mechanize
import os
import os.path as path

from datetime import datetime
from .unzip import unzip_chromediver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from jinja2 import Template
from .utils import expand_shadow_element


class ColaboHash(object):
    def __init__(
        self,
        google_email,
        google_password,
        headless=True,
        terminate_on_finish=True,
        keep_open=False,
    ):
        self.google_email = google_email
        self.google_password = google_password
        self.headless = headless
        self.terminate_on_finish = terminate_on_finish
        self.keep_open = keep_open
        self.timeout = 60

    def _setup_chromdriver(self):
        """Initializes ChromeDriver with given options"""
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument("--headless")

        chrome_options.add_argument(
            f"user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
        )
        chrome_options.add_argument("--disable-notifications")

        chromdriver_path = unzip_chromediver()
        print("Starting ChromeDriver...")
        driver = webdriver.Chrome(chromdriver_path, options=chrome_options)
        return driver, WebDriverWait(driver, self.timeout)

    def _login(self, driver, wait):
        print("Logging in...")
        driver.get("https://accounts.google.com/signin/v2/identifier")

        email = wait.until(EC.presence_of_element_located((By.NAME, "identifier")))
        email.send_keys(self.google_email)

        button_container = driver.find_element_by_xpath(
            "//div[@data-primary-action-label]"
        )
        button = button_container.find_element_by_css_selector("button")
        button.click()

        password = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
        password.send_keys(self.google_password)

        button_container = driver.find_element_by_xpath(
            "//div[@data-primary-action-label]"
        )
        button = button_container.find_element_by_css_selector("button")
        button.click()

        logged_in = wait.until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Welcome")
        )
        print("Logged in!")

    def _upload_notebook(self, driver, wait, notebook_path):
        driver.get("https://colab.research.google.com/notebooks/intro.ipynb")

        print("Sending notebook...")
        file_menu_button = wait.until(
            EC.visibility_of_element_located((By.ID, "file-menu-button"))
        )
        file_menu_button.click()

        upload_nb_menu_item = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@command='import-notebook']")
            )
        )
        upload_nb_menu_item.click()

        upload_file_container = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".upload-file-target"))
        )

        file_upload = upload_file_container.find_element_by_xpath(
            "//input[@type='file']"
        )
        file_upload.send_keys(notebook_path)

        ## Wait unitl notebook is loaded
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body"), "Colabocat")
        )

        os.remove(notebook_path)
        print("Notebook imported!")

    def _change_runtime_gpu(self, driver, wait):
        print("Changing runtime to GPU...")
        runtime_menu_button = wait.until(
            EC.visibility_of_element_located((By.ID, "runtime-menu-button"))
        )
        runtime_menu_button.click()

        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@command='change-runtime-type']")
            )
        ).click()
        wait.until(EC.visibility_of_element_located((By.ID, "accelerator"))).send_keys(
            "GPU"
        )
        wait.until(EC.visibility_of_element_located((By.ID, "ok"))).click()

    def _connect_to_runtime(self, driver, wait):
        print("Connecting to Runtime...")
        connect_btn = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "colab-connect-button"))
        )
        connect_btn.click()
        connect_shadow_root = expand_shadow_element(driver, connect_btn)

        while True:
            code = connect_shadow_root.get_attribute("innerHTML")
            if "Connected" in code:
                break
            time.sleep(1)

    def _run_all_cells(self, driver, wait):
        print("Running all cells....")
        runtime_menu_button = wait.until(
            EC.visibility_of_element_located((By.ID, "runtime-menu-button"))
        )
        runtime_menu_button.click()
        runall_menu_item = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@command='runall']"))
        ).click()

        print("Waiting for notebook to start running...")
        time.sleep(5)

    def _render_notebook_with_jinja(self, hashcat_cmd, discord_webhook_url):
        notebook_path = path.join(
            path.dirname(path.abspath(__file__)), "crackbook", "crackbook.ipynb"
        )
        with open(notebook_path, "r") as f:
            template = f.read()

        tm = Template(template)
        parameterized_nb = tm.render(
            DISCORD_WEBHOOK_URL=discord_webhook_url,
            HASHCAT_CMD=hashcat_cmd,
            TERMINATE_ON_FINISH=self.terminate_on_finish,
        )

        now = datetime.now()
        parameterized_nb_path = path.join(
            path.dirname(path.abspath(__file__)),
            "crackbook",
            "crackbook-{0}.ipynb".format(now.strftime("%Y.%m.%d.%H.%M.%S")),
        )
        with open(parameterized_nb_path, "w") as f:
            f.write(parameterized_nb)

        return parameterized_nb_path

    def run_hashcat(self, hashcat_cmd, discord_webhook_url):
        driver, wait = self._setup_chromdriver()

        self._login(driver, wait)
        # self.on_login()
        notebook_path = self._render_notebook_with_jinja(hashcat_cmd, discord_webhook_url)
        self._upload_notebook(driver, wait, notebook_path)
        self._change_runtime_gpu(driver, wait)
        self._connect_to_runtime(driver, wait)
        self._run_all_cells(driver, wait)
        # self.on_notebook_start()

        if self.keep_open:
            try:
                wait.until(EC.visibility_of_element_located((By.XPATH, "//not-found-tag")))
            except TimeoutException:
                pass
        else:
            print("Okay I am done here...")
            driver.close()

