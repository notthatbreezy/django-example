import requests

from django.core.management.base import BaseCommand

from api.models import Country, City

from django.contrib.gis.geos import MultiPolygon, Point, Polygon

COUNTRIES_GEOJSON_URL = 'https://raw.githubusercontent.com/notthatbreezy/world.geo.json/master/countries.geo.json'
CITY_GEOJSON_URL = 'https://raw.githubusercontent.com/notthatbreezy/geodata/master/cities.geojson'

class Command(BaseCommand):
    help = 'Load data into database'

    def handle(self, *args, **options):
        country_features = requests.get(COUNTRIES_GEOJSON_URL).json()['features']
        city_features = requests.get(CITY_GEOJSON_URL).json()['features']

        def create_country(coords, properties, name, polygon_type):
            if polygon_type == 'Polygon':
                multipolygon_latlng = MultiPolygon([Polygon(coord_set) for coord_set in coords], srid=4326)
            else:
                multipolygon_latlng = MultiPolygon([Polygon(coord_set[0]) for coord_set in coords], srid=4326)
            multipolygon_webmercator = multipolygon_latlng.transform(3857, clone=True)
            return Country(name=name, border_latlng=multipolygon_latlng, properties=properties, border_webmercator=multipolygon_webmercator)

        countries = [create_country(country['geometry']['coordinates'], country['properties'], country['id'], country['geometry']['type'])
                     for country in country_features]

        def create_city(coords, properties, name):
            point_latlng = Point(coords, srid=4326)
            point_webmercator = point_latlng.transform(3857, clone=True)
            return City(name=name, location_latlng=point_latlng, location_webmercator=point_webmercator, properties=properties)

        cities = [create_city(city['geometry']['coordinates'], city['properties'], city['id']) for city in city_features]

        Country.objects.bulk_create(countries)
        City.objects.bulk_create(cities)