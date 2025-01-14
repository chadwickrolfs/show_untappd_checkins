from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

from .models import Checkins
from .forms import CheckCheckinsForm

import requests


class IndexView(generic.TemplateView):
    template_name = "sci/index.html"


class CheckinsView(generic.ListView):
    model = Checkins
    template_name = "sci/checkins.html"
    ordering = "-checkin_id"


def check_checkins(request):
    if request.method == "POST":
        form = CheckCheckinsForm(request.POST)
        if form.is_valid():
            hostname = form.cleaned_data["hostname"]
            port = form.cleaned_data["port"]
            path = form.cleaned_data["path"]
            try:
                response = requests.get(f"{hostname}:{port}{path}", timeout=5)
                updated_checkins = response.json()
            except requests.exceptions.ConnectionError as e:
                print(f"connection error:\n{e}")
                return HttpResponseRedirect("")

            db_checkin_ids = {}
            db_checkins = Checkins.objects.all()
            if db_checkins:
                db_checkin_ids = dict.fromkeys([
                    db_checkins.checkin_id
                    for checkin in db_checkins
                ])

            missing_checkin_keys = (
                updated_checkins.keys() ^ db_checkin_ids.keys()
            )
            for missing_key in missing_checkin_keys:
                updated_checkin = updated_checkins[missing_key]
                updated_checkin["checkin_datetime"] = datetime.strptime(
                    updated_checkin["checkin_datetime"],
                    "%a, %d %b %Y %X %z",
                )
                new_checkin = Checkins(**updated_checkin)
                new_checkin.save()

            return HttpResponseRedirect("")
    else:
        form = CheckCheckinsForm()

    return render(request, "sci/check_checkins.html", {"form": form})
