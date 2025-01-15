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


async def check_checkins(request):
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
                error_message = f"connection error:\n{e}"
                return render(
                    request,
                    "sci/check_checkins.html",
                    {
                        "error_message": error_message,
                        "form": form
                    },
                )

            db_checkin_ids = {}
            db_checkin_id_list = []
            async for checkin in (
                Checkins.objects.all().order_by("-checkin_id")
            ):
                db_checkin_id_list.append(checkin.checkin_id)
            if db_checkin_id_list:
                db_checkin_ids = dict.fromkeys(db_checkin_id_list)

            # db_checkins = Checkins.objects.all().order_by("-checkin_id")
            # if db_checkins:
            #     db_checkin_ids = dict.fromkeys([
            #         checkin.checkin_id for checkin in db_checkins
            #     ])

            dbck = [int(k) for k in db_checkin_ids.keys()]
            udck = [int(k) for k in updated_checkins.keys()]
            missing_checkin_keys = set(udck) - set(dbck)
            for missing_key in missing_checkin_keys:
                updated_checkin = updated_checkins[missing_key]
                updated_checkin["checkin_datetime"] = datetime.strptime(
                    updated_checkin["checkin_datetime"],
                    "%a, %d %b %Y %X %z",
                )
                new_checkin = Checkins(**updated_checkin)
                new_checkin.save()
    else:
        form = CheckCheckinsForm()

    return render(request, "sci/check_checkins.html", {"form": form})
