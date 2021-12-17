from selenium import webdriver
from selenium.webdriver.common.by import By


class TestWebpages:
    def setup_method(self, method):
        self.driver = webdriver.Firefox()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_text_loaded(self):
        self.driver.get("http://localhost:8081/")
        self.driver.set_window_size(1920, 1053)
        assert self.driver.find_element(By.CSS_SELECTOR, "center").text.startswith("Hello, It works !!!")
        elements = self.driver.find_elements(By.LINK_TEXT, "do external links work?")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.LINK_TEXT, "do simple relative internal links work?")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.LINK_TEXT, "do general relative links work")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.LINK_TEXT, "do simple absolute links work")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.LINK_TEXT, "do general absolute links work")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.LINK_TEXT, "do URLs with spaces work")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.LINK_TEXT, "do URLs with %20 work")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.LINK_TEXT, "do TXT files work")
        assert len(elements) > 0

    def test_images_loaded(self):
        self.driver.get("http://localhost:8081/")
        self.driver.set_window_size(1920, 1053)
        elements = self.driver.find_elements(By.CSS_SELECTOR, "tr:nth-child(1) img")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "tr:nth-child(2) img")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "tr:nth-child(3) img")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "tr:nth-child(4) img")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "tr:nth-child(5) img")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "tr:nth-child(6) img")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "tr:nth-child(7) img")
        assert len(elements) > 0

    def test_external_links(self):
        self.driver.get("http://localhost:8081/")
        self.driver.set_window_size(1920, 1053)
        self.driver.find_element(By.LINK_TEXT, "do external links work?").click()
        assert self.driver.current_url.startswith("https://www.google.com/")

    def test_simple_relative_internal_links(self):
        self.driver.get("http://localhost:8081/")
        self.driver.set_window_size(1920, 1053)
        self.driver.find_element(By.LINK_TEXT, "do simple relative internal links work?").click()
        assert self.driver.current_url == "http://localhost:8081/b.html"
        self.driver.find_element(By.LINK_TEXT, "back").click()
        assert self.driver.current_url == "http://localhost:8081/a.html"

    def test_general_relative_internal_links(self):
        self.driver.get("http://localhost:8081/")
        self.driver.set_window_size(1920, 1053)
        self.driver.find_element(By.LINK_TEXT, "do general relative links work").click()
        assert self.driver.current_url == "http://localhost:8081/aaa/b.html"
        self.driver.find_element(By.LINK_TEXT, "c").click()
        assert self.driver.current_url == "http://localhost:8081/aaa/c.html"
        self.driver.find_element(By.LINK_TEXT, "back").click()
        assert self.driver.current_url == "http://localhost:8081/a.html"

    def test_simple_absolute_link(self):
        self.driver.get("http://localhost:8081/")
        self.driver.set_window_size(1920, 1053)
        self.driver.find_element(By.LINK_TEXT, "do simple absolute links work").click()
        assert self.driver.current_url == "http://localhost:8081/c.html"

    def test_general_absolute_link(self):
        self.driver.get("http://localhost:8081/")
        self.driver.set_window_size(1920, 1053)
        self.driver.find_element(By.LINK_TEXT, "do general absolute links work").click()
        assert self.driver.current_url == "http://localhost:8081/aaa/bbb/c.html"
        self.driver.find_element(By.LINK_TEXT, "back").click()
        assert self.driver.current_url == "http://localhost:8081/a.html"

    def test_url_with_spaces(self):
        self.driver.get("http://localhost:8081/")
        self.driver.set_window_size(1920, 1053)
        self.driver.find_element(By.LINK_TEXT, "do URLs with spaces work").click()
        assert self.driver.current_url == "http://localhost:8081/a%20b.html"
        self.driver.find_element(By.LINK_TEXT, "back").click()
        assert self.driver.current_url == "http://localhost:8081/a.html"

    def test_url_with_special_characters(self):
        self.driver.get("http://localhost:8081/")
        self.driver.set_window_size(1920, 1053)
        self.driver.find_element(By.LINK_TEXT, "do URLs with %20 work").click()
        assert self.driver.current_url == "http://localhost:8081/a%20b.html"
        self.driver.find_element(By.LINK_TEXT, "back").click()
        assert self.driver.current_url == "http://localhost:8081/a.html"

    def test_txt_file(self):
        self.driver.get("http://localhost:8081/")
        self.driver.set_window_size(1920, 1053)
        self.driver.find_element(By.LINK_TEXT, "do TXT files work").click()
        assert self.driver.current_url == "http://localhost:8081/a.txt"
        assert self.driver.find_element(By.TAG_NAME, "body").text == "Hello TXT works"
