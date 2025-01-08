from django.views import generic

from .models import Checkins


class IndexView(generic.ListView):
    template_name = "sci/index.html"


class CheckinsView(generic.ListView):
    model = Checkins
    template_name = "sci/checkins.html"
