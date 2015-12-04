from api.models import City, Country

from django.contrib.gis.db.models.functions import Area

Country.objects.annotate(area=Area('border_webmercator')).order_by('-area')

City.objects.filter(properties__wikipedia='Seattle')
