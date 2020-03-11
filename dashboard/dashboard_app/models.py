from django.db import models


class MigrationEntry(models.Model):
    _from = models.CharField(max_length=20)
    _to = models.CharField(max_length=20)
    _date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self._date.day}-{self._date.month}-{self._date.year},{self._date.hour},{self._date.minute},{self._date.second}:\tfrom:{self._from}\tto:{self._to}."
