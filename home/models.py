from django.db import models

# Create your models here.
class RawMaterial(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Spot(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name 

class SpotRawMaterial(models.Model):
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    is_active    = models.BooleanField(default=True)

    def __str__(self):
        return str(self.spot.name) + " - " + str(self.raw_material.name)     

class Industry(models.Model):
    name = models.CharField(max_length=50)
    spot = models.ForeignKey(Spot, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Route(models.Model):
    from_spot = models.ForeignKey(Spot, related_name="From", on_delete=models.CASCADE)
    to_spot   = models.ForeignKey(Spot, related_name="To", on_delete=models.CASCADE)
    distace   = models.IntegerField()

    def __str__(self):
        return str(self.from_spot) + " -> " + str(self.to_spot) + " = " + str(self.distace)
