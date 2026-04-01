from django.db import models

class Worker(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    daily_income = models.IntegerField()

class Policy(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    premium = models.IntegerField()
    payout = models.IntegerField(default=500)