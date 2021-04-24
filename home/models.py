from django.db import models

# Create your models here.
class Item(models.Model): #Raw materials + product
    name = models.CharField(max_length=50)
    product = models.BooleanField(default=False)
    raw_material = models.BooleanField(default=False)
    product_cost = models.IntegerField(default=0)
    raw_material_cost = models.IntegerField(default=0)
    category_1 = models.BooleanField(default=False)
    category_2 = models.BooleanField(default=False)
    category_3 = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Spot(models.Model):
    name = models.CharField(max_length=50)
    tax = models.IntegerField(default=0)
    lat = models.CharField(max_length=50, default='0')
    lng = models.CharField(max_length=50, default='0')
    def __str__(self):
        return self.name 

class SpotRawMaterial(models.Model):
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(Item, limit_choices_to={'raw_material':True}, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    is_active    = models.BooleanField(default=True)

    def __str__(self):
        return str(self.spot.name) + " - " + str(self.raw_material.name)     

class Industry(models.Model):
    name = models.CharField(max_length=50)
    spot = models.ForeignKey(Spot, on_delete=models.SET_NULL, null=True, blank=True)
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Route(models.Model):
    from_spot = models.ForeignKey(Spot, related_name="From", on_delete=models.CASCADE)
    to_spot   = models.ForeignKey(Spot, related_name="To", on_delete=models.CASCADE)
    distace   = models.IntegerField()

    def __str__(self):
        return str(self.from_spot) + " -> " + str(self.to_spot) + " = " + str(self.distace)


class Manufacture(models.Model):
    product = models.ForeignKey(Item, related_name='Product', limit_choices_to={'product':True}, on_delete=models.SET_NULL, null=True, blank=True)
    raw_material = models.ForeignKey(Item, related_name='RawMaterial', limit_choices_to={'raw_material':True}, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.product) + " -> " + str(self.raw_material) + " = " + str(self.quantity)


class Notification(models.Model):

    notice = models.CharField(max_length=500)
    def __str__(self):
        return self.notice


class Season(models.Model):
    season_1 = models.BooleanField(default=False)
    season_2 = models.BooleanField(default=False)
    season_3 = models.BooleanField(default=False)
    season_4 = models.BooleanField(default=False)
