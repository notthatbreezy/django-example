from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.http import JsonResponse

from api.models import Country, City


class CountryView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Country
    response_class = JsonResponse

    def handle_no_permission(self):
        return JsonResponse({'detail': 'Access Denied'}, status=403)

    def test_func(self):
        return self.request.user.username.startswith('t')

    def render_to_response(self, context, **response_kwargs):
        features = [obj.as_dict for obj in self.get_queryset()]
        return JsonResponse({'type': 'FeatureCollection', 'features': features}, safe=False)


class CityView(ListView):
    model = City
    response_class = JsonResponse

    def render_to_response(self, context, **response_kwargs):
        features = [obj.as_dict for obj in self.get_queryset()]
        return JsonResponse({'type': 'FeatureCollection', 'features': features}, safe=False)
