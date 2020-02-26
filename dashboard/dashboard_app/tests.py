import json
from django.test import TestCase, Client
import unittest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from dashboard_app.models import MigrationEntry
from django.urls import reverse
import socket
import time
import datetime

# file that stores the general information of the app provided by the Driver
from dashboard.settings import GENERAL_INFO_FILE


# Decorator for skipping a test
def skip_test(self):
    pass


# Decorator for printing the test's name
def print_test_name(self):
    print(self.__name__)
    return self


@skip_test
class GeneralInformationSimpleTests(unittest.TestCase):
    """Tests accuracy of information passed in context dictionary"""

    @classmethod
    def setUpClass(cls):
        # Every test needs a client.
        cls.client = Client()

        # For this TestCase we only need one migration entry
        MigrationEntry.objects.create(_to="AWS", _from="AZURE", _date=datetime.date(year=2020, month=2, day=3))

        # Issue a GET request.
        cls.response = cls.client.get('/dashboard/')

    def setUp(self):
        pass

    def test_details(self):
        # Check that the response is 200 OK.
        self.assertEqual(self.__class__.response.status_code, 200)

    def test_last_migration(self):
        """Ensure last migration date is correct in context"""
        entry = MigrationEntry.objects.last()
        self.assertEqual(self.__class__.response.context.get('last_migration', None), entry._date.strftime("%d/%m/%Y"))
        print("Number of entries in database: " + str(MigrationEntry.objects.count()))

    def test_current_date(self):
        """Ensure current date is correct in context"""
        self.assertEqual(self.__class__.response.context.get('current_date', None),
                         datetime.date.today().strftime("%d/%m/%Y"))

    def test_current_ip(self):
        """Ensure current IP address is correct in context"""
        with open(GENERAL_INFO_FILE, "r") as jsonFile:
            general_info_json = json.load(jsonFile)

        self.assertEqual(self.__class__.response.context.get('current_ip', None),
                         general_info_json.get('GLAROS_CURRENT_IP'))


class GeneralInformationLiveServerTests(StaticLiveServerTestCase):
    """Tests the validity of information displayed on the general information section"""

    @classmethod
    def setUpClass(cls):
        cls.host = socket.gethostbyname(socket.gethostname())
        super(GeneralInformationLiveServerTests, cls).setUpClass()
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('headless')
        cls.browser = webdriver.Chrome(chrome_options=chrome_options)
        cls.browser.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        MigrationEntry.objects.create(_to="AWS", _from="AZURE", _date=datetime.date(year=2020, month=2, day=3))

    def tearDown(self):
        MigrationEntry.objects.all().delete()

    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)

    def test_there_is_a_general_info_section(self):
        """Ensure there is a General Information section in the rendered dashboard"""
        # Go to Dashboard page
        self.browser.get(self.get_full_url('index'))

        # Check if body now has General Information Area/Section
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn("General Information".lower(), body.text.lower())

    def test_current_date(self):
        """Ensure current (today's) date is correct in the rendered dashboard"""
        # Go to Dashboard page
        self.browser.get(self.get_full_url('index'))

        # Check if the current date is correct
        current_date_text = self.browser.find_element_by_id('current_date').text
        self.assertEqual(current_date_text, datetime.date.today().strftime("%d/%m/%Y"),
                         "Current (today's) date on the dashboard is wrong.")

    def test_check_last_migration(self):
        """Ensure last migration date is correct in the rendered dashboard"""
        # Go to Dashboard page
        self.browser.get(self.get_full_url('index'))

        # Check if the last migration mathes that of the last MigrationEntry
        last_migration_text = self.browser.find_element_by_id('last_migration').text
        self.assertEqual(last_migration_text, MigrationEntry.objects.last()._date.strftime("%d/%m/%Y"),
                         "Last Migration date on the dashboard is wrong.")

    def test_current_ip(self):
        """Ensure current IP address is correct in the rendered dashboard"""
        with open(GENERAL_INFO_FILE, "r") as jsonFile:
            general_info_json = json.load(jsonFile)

        # Check if the current date is correct
        current_ip_text = self.browser.find_element_by_id('current_ip').text
        self.assertEqual(current_ip_text, general_info_json.get('GLAROS_CURRENT_IP'),
                         "Current ip on the dashboard is wrong.")


class TestStockPricesSection(unittest.TestCase):
    """Tests the validity of the stocks graph"""

    @classmethod
    def setUpClass(cls):
        # Every test needs a client.
        cls.client = Client()

        # For this TestCase we only need one migration entry
        MigrationEntry.objects.create(_to="AWS", _from="AZURE", _date=datetime.date(year=2020, month=2, day=3))

        # Issue a GET request.
        cls.response = cls.client.get('/dashboard/')

    def setUp(self):
        self.a = 1

    def tearDown(self):
        del self.a

    def get_N_stock_entries(self, N):
        """Helper method to get stock prices from server via ajax calls"""
        request_data = {
            'points': N,
            'interval': '1d',  # daily interval (not important for this test)
        }
        response = self.client.get(reverse('ajax_update_stock_prices'), request_data)
        return response

    def test_ajax_for_stocks_returns_10_entries(self):
        response = self.get_N_stock_entries(10)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        for dataset in response_data.get('datasets', {'data': []}):  # in case no datasets are returned -> fail the test
            self.assertTrue(len(dataset['data']), 10)

    def test_ajax_for_stocks_returns_20_entries(self):
        response = self.get_N_stock_entries(20)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        for dataset in response_data.get('datasets', {'data': []}):  # in case no datasets are returned -> fail the test
            self.assertTrue(len(dataset['data']), 20)

    def test_ajax_for_stocks_returns_30_entries(self):
        response = self.get_N_stock_entries(20)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        for dataset in response_data.get('datasets', {'data': []}):  # in case no datasets are returned -> fail the test
            self.assertTrue(len(dataset['data']), 20)


@skip_test
class TestMigrationTimeline(TestCase):
    """Tests the validity of the migration timeline"""

    def setUp(self):
        self.a = 1

    def tearDown(self):
        del self.a

    def test_basic1(self):
        """Basic with setup"""
        self.assertNotEqual(self.a, 2)

    def test_basic2(self):
        """Basic with setup"""
        assert self.a != 2

    def test_fail(self):
        """Basic with setup"""
        assert self.a == 2


@skip_test
class TestMigrationHistoryTable(TestCase):
    """Tests the validity of information provided by the migration table"""

    def setUp(self):
        self.a = 1

    def tearDown(self):
        del self.a

    def test_basic1(self):
        """Basic with setup"""
        self.assertNotEqual(self.a, 2)

    def test_basic2(self):
        """Basic with setup"""
        assert self.a != 2

    def test_fail(self):
        """Basic with setup"""
        assert self.a == 2
