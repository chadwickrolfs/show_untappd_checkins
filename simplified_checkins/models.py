from django.db import models


class Checkins(models.Model):
    checkin_id = models.IntegerField()
    checkin_datetime = models.DateTimeField()
    checkin_comment = models.CharField(max_length=999)
    beer_bid = models.IntegerField()
    beer_name = models.CharField(max_length=500)
    beer_abv = models.DecimalField(max_digits=4, decimal_places=2)
    beer_style = models.CharField(max_length=250)
    brewery_id = models.IntegerField()
    brewery_name = models.CharField(max_length=500)
    brewery_country = models.CharField(max_length=250)
    brewery_city = models.CharField(max_length=250)
    brewery_latitude = models.IntegerField()
    brewery_longitude = models.IntegerField()
    venue_id = models.IntegerField()
    venue_name = models.CharField(max_length=500)
    venue_address = models.CharField(max_length=500)
    venue_city = models.CharField(max_length=250)
    venue_country = models.CharField(max_length=250)
    venue_latitude = models.IntegerField()
    venue_longitude = models.IntegerField()

    def __str__(self):
        return f"{self.beer_name} by {self.brewery_name}"
