from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from users.tests.factories import VoluntaryFactory, UserFactory
from django.urls import reverse
from events.tests.factories import EventFactory
from events.models import Event
import time


class TestLogin(StaticLiveServerTestCase):

    def setUp(self):
        options = Options()
        # options.add_argument("--headless")
        self.user = UserFactory(is_employee=True)
        self.voluntary = VoluntaryFactory(user__is_voluntary=True)
        self.password = 'django01'
        self.user.set_password(self.password)
        self.user.save()
        self.driver = webdriver.Chrome(
            options=options, executable_path='/home/mikael/projetos/aprepi/aprepi-django/tests/chromedriver')
        self.vars = {}

        self.driver.get(self.live_server_url)
        self.driver.set_window_size(1366, 728)
        self.driver.find_element(
            By.CSS_SELECTOR, "a:nth-child(4) > .uk-button").click()
        self.driver.find_element(
            By.ID, "id_username").send_keys(self.user.username)
        self.driver.find_element(By.ID, "id_password").send_keys(self.password)
        self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)

    def teardown_method(self, method):
        self.driver.quit()

    def test_flow_list_and_update_event(self):
        events = EventFactory.create_batch(5)
        self.driver.get(self.live_server_url + reverse("events:list"))
        update_url = reverse("events:update", kwargs={"pk": events[0].id})

        self.driver.find_element(By.CSS_SELECTOR, f"a.uk-link-text[href$='{update_url}']").click()

        self.driver.find_element(By.ID, "id_start_date").click()
        self.driver.find_element(By.ID, "id_start_date").send_keys("26-06-2021")
        self.driver.find_element(By.ID, "id_end_date").click()
        self.driver.find_element(By.ID, "id_end_date").send_keys("27-06-2021")

        self.driver.find_element(By.CSS_SELECTOR, "body > div > div > form > button").click()

    def test_flow_create_and_delete_event(self):
        event_name = "Um novo evento"
        self.driver.find_element(
            By.CSS_SELECTOR, "div:nth-child(2) > .uk-card .uk-card-title").click()
        title_content = self.driver.find_element(
            By.CSS_SELECTOR, " body > div > div > form > fieldset > legend").text

        self.assertEqual(title_content, 'Cadastro de evento')

        self.driver.find_element(By.ID, "id_event_name").click()
        self.driver.find_element(By.ID, "id_event_name").send_keys(event_name)
        self.driver.find_element(By.ID, "id_start_date").click()
        self.driver.find_element(By.ID, "id_start_date").send_keys("24-06-2021")
        self.driver.find_element(By.ID, "id_end_date").click()
        self.driver.find_element(By.ID, "id_end_date").send_keys("25-06-2021")
        self.driver.find_element(By.CSS_SELECTOR, ".uk-margin:nth-child(6)").click()
        dropdown = self.driver.find_element(By.ID, "id_volunteers")
        dropdown.find_element(By.XPATH, f"//option[. = '{self.voluntary}']").click()
        self.driver.find_element(By.ID, "id_event_details").click()
        self.driver.find_element(By.ID, "id_event_details").send_keys("Evento fechado para pessoas com cadastro")
        self.driver.find_element(By.CSS_SELECTOR, "body > div > div > form > button").click()

        event_obj = Event.objects.get(event_name=event_name)
        self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) svg").click()
        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, f"#modal-{event_obj.id} > div > p.uk-text-right > button.uk-button.uk-button-danger").click()
        # self.driver.find_element(By.LINK_TEXT, "feijoada aprepi ii").click()

    def test_delete_event(self):
        events = EventFactory.create_batch(5)
        self.driver.get(self.live_server_url + reverse("events:list"))

        self.driver.find_element(By.CSS_SELECTOR, f"a.uk-button-danger[href$='#modal-{events[0].id}']").click()
        self.driver.find_element(By.CSS_SELECTOR, f"#modal-{events[0].id} > div > p.uk-text-right > button.uk-button.uk-button-danger").click()
        self.assertEqual(Event.objects.count(), 4)
