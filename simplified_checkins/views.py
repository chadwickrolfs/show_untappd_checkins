from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

from .models import Checkins
from .forms import CheckCheckinsForm

import requests


class IndexView(generic.ListView):
    template_name = "sci/index.html"


class CheckinsView(generic.ListView):
    model = Checkins
    template_name = "sci/checkins.html"


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
            db_checkins = Checkins.objects.all()

            checkin_ids = [
                checkin["checkin_id"]
                for checkin in updated_checkins
            ]
            db_checkin_ids = [
                db_checkins.checkin_id
                for checkin in db_checkins
            ]
            indexes = [
                checkin_ids.index(missing_id)
                for missing_id in set(checkin_ids) ^ set(db_checkin_ids)
            ]
            missing_checkins = [updated_checkins[index] for index in indexes]
            for missing_checkin in missing_checkins:
                new_checkin = Checkins(missing_checkins)
                new_checkin.save()

            return HttpResponseRedirect("")
    else:
        form = CheckCheckinsForm()

    return render(request, "sci/check_checkins.html", {"form": form})
