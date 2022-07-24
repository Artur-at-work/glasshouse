from django.db import models

class PriceHistory(models.Model):
    #house_id = models.ForeignKey('House', on_delete=models.CASCADE)
    house_id = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    rec_date = models.DateField()

    def __str__(self):
        return self.house_id

