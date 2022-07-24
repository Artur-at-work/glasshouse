from django.db import models

class TaiwanCity(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True, default="Taiwan")
    
    def __str__(self):
        return str(self.name)

class TaiwanDistrict(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    city = models.ForeignKey(TaiwanCity, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.city}-{self.name}"
