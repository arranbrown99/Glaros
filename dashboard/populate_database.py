from dashboard_app.models import MigrationEntry
import os
import django
from datetime import date
from collections import namedtuple
import datetime
import sqlite3
import random


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

django.setup()


ME = namedtuple('MigrationEntry', 'Date From To')

# How Google Charts accepts the date
# ['AWS', new Date(2015, 10, 1), new Date(2015, 10, 3)],
# ['Azure', new Date(2015, 10, 3), new Date(2015, 10, 5)],
# ['GCP', new Date(2015, 10, 5), new Date(2015, 10, 7)],
# ['AWS', new Date(2015, 10, 7), new Date(2015, 10, 14)],
# ['GCP', new Date(2015, 10, 14), new Date(2015, 10, 16)],
# ['Azure', new Date(2015, 10, 16), new Date(2015, 10, 20)],
# ['AWS', new Date(2015, 10, 20), new Date(2015, 10, 25)],
# ['GCP', new Date(2015, 10, 25), new Date(2015, 10, 29)],
# ['Azure', new Date(2015, 10, 29), new Date(2015, 10, 30)],
# ['AWS', new Date(2015, 10, 30), new Date(2015, 11, 6)],


def populate():
    csps = [
        ('Aws', 'Azure'),
        ('Azure', 'Google'),
        ('Google', 'Aws'),
    ]
    for i in range(20):
        hours_offset = i * 10
        cps_pair = csps[i % 3]

        database_entry(cps_pair[0], cps_pair[1], hours_offset)

    print("all!")
    print(MigrationEntry.objects.all())

    print("Finished!")


def add_migration_entry(_date, _from, _to):
    me = MigrationEntry.objects.get_or_create(
        _date=_date, _from=_from, _to=_to)[0]
    me._date = _date
    me.save()
    return me


def database_entry(currently_on, moving_to, hours_offset):
    """

    Update information about time and location of migration for front end

    Parameters
    ----------
    moving_to: the CSP we are moving to
    currently_on : the CSP we are currently on
    """
    # Log migration to database
    connection = None
    try:
        now = datetime.datetime.now()\
            - datetime.timedelta(hours=21*10)\
            + datetime.timedelta(hours=hours_offset,
                                 minutes=random.randint(1, 59))
        connection = sqlite3.connect('./db.sqlite3')
        print("The sqlite3 connection is established.")
        cursor = connection.cursor()
        insert_query = """ INSERT INTO dashboard_app_migrationentry (_from,_to,_date) VALUES ('%s', '%s', '%s')""" \
                       % (currently_on, moving_to,
                          now)
        cursor.execute(insert_query)
        connection.commit()
        cursor.close()

    except sqlite3.Error as e:
        raise e
    finally:
        if connection:
            connection.close()
            print("The sqlite3 connection is now closed.")


# Start execution here!
if __name__ == '__main__':
    print("Starting dashboard population script...")
    populate()
