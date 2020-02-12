import os
from datetime import date
from collections import namedtuple

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

import django

django.setup()

from dashboard_app.models import MigrationEntry

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

dummy_entries = [
    ME(date(2017, 1, 3), 'AZURE', 'GCP'),
    ME(date(2017, 1, 4), 'GCP', 'AWS'),
    ME(date(2017, 1, 5), 'AWS', 'GCP'),
    ME(date(2017, 1, 6), 'GCP', 'AZURE'),
    ME(date(2017, 1, 7), 'AZURE', 'AWS'),
    ME(date(2017, 1, 9), 'AWS', 'GCP'),
    ME(date(2017, 1, 10), 'GCP', 'AZURE'),
    ME(date(2017, 1, 11), 'AZURE', 'AWS'),
    ME(date(2017, 11, 12), 'AWS', 'AZURE'),
    ME(date(2017, 11, 13), 'AZURE', 'GCP'),
    ME(date(2017, 11, 14), 'GCP', 'AWS'),
    ME(date(2017, 11, 15), 'AWS', 'GCP'),
    ME(date(2017, 11, 16), 'GCP', 'AZURE'),
    ME(date(2017, 11, 17), 'AZURE', 'AWS'),
    ME(date(2017, 11, 19), 'AWS', 'GCP'),
    ME(date(2017, 11, 20), 'GCP', 'AZURE'),
    ME(date(2017, 11, 21), 'AZURE', 'AWS'),
    ME(date(2017, 11, 22), 'AWS', 'AZURE'),
    ME(date(2017, 11, 23), 'AZURE', 'GCP'),
    ME(date(2017, 11, 24), 'GCP', 'AWS'),
    ME(date(2017, 11, 25), 'AWS', 'GCP'),
    ME(date(2017, 11, 26), 'GCP', 'AZURE'),
    ME(date(2017, 11, 27), 'AZURE', 'AWS'),
    ME(date(2017, 11, 29), 'AWS', 'GCP'),
    ME(date(2017, 11, 30), 'GCP', 'AZURE'),
    ME(date(2017, 12, 1), 'AZURE', 'AWS'),
    ME(date(2017, 12, 2), 'AWS', 'AZURE'),
    ME(date(2017, 12, 3), 'AZURE', 'GCP'),
    ME(date(2017, 12, 4), 'GCP', 'AWS'),
    ME(date(2017, 12, 5), 'AWS', 'GCP'),
    ME(date(2017, 12, 6), 'GCP', 'AZURE'),
    ME(date(2017, 12, 7), 'AZURE', 'AWS'),
    ME(date(2017, 12, 9), 'AWS', 'GCP'),
    ME(date(2017, 12, 20), 'GCP', 'AZURE'),
    ME(date(2017, 12, 21), 'AZURE', 'AWS'),
    ME(date(2018, 1, 2), 'AWS', 'AZURE'),
    ME(date(2018, 1, 3), 'AZURE', 'GCP'),
    ME(date(2018, 1, 4), 'GCP', 'AWS'),
    ME(date(2018, 1, 5), 'AWS', 'GCP'),
    ME(date(2018, 1, 6), 'GCP', 'AZURE'),
    ME(date(2018, 1, 7), 'AZURE', 'AWS'),
    ME(date(2018, 1, 9), 'AWS', 'GCP'),
    ME(date(2018, 1, 10), 'GCP', 'AZURE'),
    ME(date(2018, 1, 11), 'AZURE', 'AWS'),
    ME(date(2018, 1, 12), 'AWS', 'AZURE'),
    ME(date(2018, 1, 13), 'AZURE', 'GCP'),
    ME(date(2018, 1, 14), 'GCP', 'AWS'),
    ME(date(2018, 1, 15), 'AWS', 'GCP'),
    ME(date(2018, 1, 16), 'GCP', 'AZURE'),
    ME(date(2018, 1, 17), 'AZURE', 'AWS'),
    ME(date(2018, 1, 19), 'AWS', 'GCP'),
    ME(date(2018, 1, 20), 'GCP', 'AZURE'),
    ME(date(2018, 1, 21), 'AZURE', 'AWS'),
    ME(date(2018, 1, 22), 'AWS', 'AZURE'),
    ME(date(2018, 1, 23), 'AZURE', 'GCP'),
    ME(date(2018, 1, 24), 'GCP', 'AWS'),
    ME(date(2018, 1, 25), 'AWS', 'GCP'),
    ME(date(2018, 1, 26), 'GCP', 'AZURE'),
    ME(date(2018, 1, 27), 'AZURE', 'AWS'),
    ME(date(2018, 1, 29), 'AWS', 'GCP'),
    ME(date(2018, 1, 30), 'GCP', 'AZURE'),
    ME(date(2018, 2, 1), 'AZURE', 'AWS'),
    ME(date(2018, 2, 2), 'AWS', 'AZURE'),
    ME(date(2019, 1, 3), 'AZURE', 'GCP'),
    ME(date(2019, 1, 4), 'GCP', 'AWS'),
    ME(date(2019, 1, 5), 'AWS', 'GCP'),
    ME(date(2019, 1, 6), 'GCP', 'AZURE'),
    ME(date(2019, 1, 7), 'AZURE', 'AWS'),
    ME(date(2019, 1, 9), 'AWS', 'GCP'),
    ME(date(2019, 1, 10), 'GCP', 'AZURE'),
    ME(date(2019, 1, 11), 'AZURE', 'AWS'),
    ME(date(2019, 11, 12), 'AWS', 'AZURE'),
    ME(date(2019, 11, 13), 'AZURE', 'GCP'),
    ME(date(2019, 11, 14), 'GCP', 'AWS'),
    ME(date(2019, 11, 15), 'AWS', 'GCP'),
    ME(date(2019, 11, 16), 'GCP', 'AZURE'),
    ME(date(2019, 11, 17), 'AZURE', 'AWS'),
    ME(date(2019, 11, 19), 'AWS', 'GCP'),
    ME(date(2019, 11, 20), 'GCP', 'AZURE'),
    ME(date(2019, 11, 21), 'AZURE', 'AWS'),
    ME(date(2019, 11, 22), 'AWS', 'AZURE'),
    ME(date(2019, 11, 23), 'AZURE', 'GCP'),
    ME(date(2019, 11, 24), 'GCP', 'AWS'),
    ME(date(2019, 11, 25), 'AWS', 'GCP'),
    ME(date(2019, 11, 26), 'GCP', 'AZURE'),
    ME(date(2019, 11, 27), 'AZURE', 'AWS'),
    ME(date(2019, 11, 29), 'AWS', 'GCP'),
    ME(date(2019, 11, 30), 'GCP', 'AZURE'),
    ME(date(2019, 12, 1), 'AZURE', 'AWS'),
    ME(date(2019, 12, 2), 'AWS', 'AZURE'),
    ME(date(2019, 12, 3), 'AZURE', 'GCP'),
    ME(date(2019, 12, 4), 'GCP', 'AWS'),
    ME(date(2019, 12, 5), 'AWS', 'GCP'),
    ME(date(2019, 12, 6), 'GCP', 'AZURE'),
    ME(date(2019, 12, 7), 'AZURE', 'AWS'),
    ME(date(2019, 12, 9), 'AWS', 'GCP'),
    ME(date(2019, 12, 20), 'GCP', 'AZURE'),
    ME(date(2019, 12, 21), 'AZURE', 'AWS'),
    ME(date(2020, 1, 2), 'AWS', 'AZURE'),
    ME(date(2020, 1, 3), 'AZURE', 'GCP'),
    ME(date(2020, 1, 4), 'GCP', 'AWS'),
    ME(date(2020, 1, 5), 'AWS', 'GCP'),
    ME(date(2020, 1, 6), 'GCP', 'AZURE'),
    ME(date(2020, 1, 7), 'AZURE', 'AWS'),
    ME(date(2020, 1, 9), 'AWS', 'GCP'),
    ME(date(2020, 1, 10), 'GCP', 'AZURE'),
    ME(date(2020, 1, 11), 'AZURE', 'AWS'),
    ME(date(2020, 1, 12), 'AWS', 'AZURE'),
    ME(date(2020, 1, 13), 'AZURE', 'GCP'),
    ME(date(2020, 1, 14), 'GCP', 'AWS'),
    ME(date(2020, 1, 15), 'AWS', 'GCP'),
    ME(date(2020, 1, 16), 'GCP', 'AZURE'),
    ME(date(2020, 1, 17), 'AZURE', 'AWS'),
    ME(date(2020, 1, 19), 'AWS', 'GCP'),
    ME(date(2020, 1, 20), 'GCP', 'AZURE'),
    ME(date(2020, 1, 21), 'AZURE', 'AWS'),
    ME(date(2020, 1, 22), 'AWS', 'AZURE'),
    ME(date(2020, 1, 23), 'AZURE', 'GCP'),
    ME(date(2020, 1, 24), 'GCP', 'AWS'),
    ME(date(2020, 1, 25), 'AWS', 'GCP'),
    ME(date(2020, 1, 26), 'GCP', 'AZURE'),
    ME(date(2020, 1, 27), 'AZURE', 'AWS'),
    ME(date(2020, 1, 29), 'AWS', 'GCP'),
    ME(date(2020, 1, 30), 'GCP', 'AZURE'),
    ME(date(2020, 2, 1), 'AZURE', 'AWS'),
    ME(date(2020, 2, 2), 'AWS', 'AZURE'),
]


def populate():
    for entry in dummy_entries:
        # d, f, t = entry
        print(entry)
        add_migration_entry(_date=entry.Date, _from=entry.From, _to=entry.To)

    print("all!")
    print(MigrationEntry.objects.all())

    print("Finished!")


def add_migration_entry(_date, _from, _to):
    me = MigrationEntry.objects.get_or_create(_date=_date, _from=_from, _to=_to)[0]
    me._date = _date
    me.save()
    return me


# Start execution here!
if __name__ == '__main__':
    print("Starting dashboard population script...")
    populate()
