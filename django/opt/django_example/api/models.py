from __future__ import unicode_literals

import json

from django.contrib.postgres.fields import JSONField
from django.contrib.gis.db import models


class Country(models.Model):
    name = models.TextField()
    border_latlng = models.MultiPolygonField(srid=4326)
    border_webmercator = models.MultiPolygonField(srid=3857)
    properties = JSONField(default=dict())

    def __str__(self):
        return 'COUNTRY CODE: {}'.format(self.name)

    @property
    def as_dict(self):
        geometry = json.loads(self.border_latlng.json)
        return dict(properties=self.properties, id=self.name, geometry=geometry, type='Feature')


class City(models.Model):
    name = models.TextField()
    location_latlng = models.PointField(srid=4326)
    location_webmercator = models.PointField(srid=4326)
    properties = JSONField()

    def __str__(self):
        return 'NAME:{}'.format(self.name)

    @property
    def as_dict(self):
        geometry = json.loads(self.location_latlng.json)
        return dict(properties=self.properties, id=self.name,
                    geometry=geometry, type='Feature')
