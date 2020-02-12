from django.test import TestCase, Client
import unittest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from dashboard_app.models import MigrationEntry
import socket
import time
import datetime


# Decorator for skipping a test
def skip_test(self):
    pass


class SimpleTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print(MigrationEntry.objects.count())
        # For this TestCase we only need one migration entry
        MigrationEntry.objects.create(_to="AWS", _from="AZURE", _date=datetime.date(year=2020, month=2, day=3))
        print(MigrationEntry.objects.count())

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get('/dashboard/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains 5 customers.
        print(response.context)
        print(response.context['current_date'] == datetime.date.today().strftime("%d/%m/%Y"))
        self.assertEqual(response.context['current_date'], datetime.date.today().strftime("%d/%m/%Y"))

# @skip_test
class GeneralInformationLiveServerTests(StaticLiveServerTestCase):
    """Tests the validity of information displayed on the general information section"""

    @classmethod
    def setUpClass(cls):
        cls.host = socket.gethostbyname(socket.gethostname())
        super(GeneralInformationLiveServerTests, cls).setUpClass()

    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.implicitly_wait(3)
        MigrationEntry.objects.create(_to="AWS", _from="AZURE", _date=datetime.date(year=2020, month=2, day=3))


    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    @skip_test
    def test_there_is_a_general_info_section(self):
        pass

    @skip_test
    def test_current_date(self):
        """Basic with setup"""
        url = self.live_server_url
        print("--->", url)
        url = url.replace('localhost', '127.0.0.1')

        self.browser.get(url + '/dashboard/')
        # time.sleep(4)
        # body = self.browser.find_element_by_tag_name('body')
        # print(body)
        # self.assertIn('General Information', body.text)

    def test_there_is_more_than_one_migration_entry(self):
        print(self)
        print("There are these many entries in the database:",MigrationEntry.objects.count())
        self.assertGreater( MigrationEntry.objects.count(), 0, "Migration model should have at least one entry")

    # THINGS TO CHECK
    # - there is a General Information section
    # - check last migration
    # - check current date
    # - check current ip



    def test_there_is_more_than_one_migration_entr2y(self):
        print(self)
        print("There are these many entries in the database:",MigrationEntry.objects.count())
        self.assertGreater( MigrationEntry.objects.count(), 0, "Migration model should have at least one entry")

    def test_there_is_more_than_one_migration_entr3y(self):
        print(self)
        print("There are these many entries in the database:",MigrationEntry.objects.count())
        self.assertGreater( MigrationEntry.objects.count(), 0, "Migration model should have at least one entry")

@skip_test
class TestStockPricesSection(TestCase):
    """Tests the validity of the stocks graph"""

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
