from django.db import models

# Create your models here.
MOVING_TYPES = (
    ('DRIVING', 'На автобусе '),
    ('WALKING', 'Пешком')
)


class PhysicalTourRoute(models.Model):

    place = models.ForeignKey('place.Platform', on_delete=models.SET_NULL, null=True)
    time_start = models.TimeField(null=True)
    time_finish = models.TimeField(null=True)
    moving_type = models.CharField(choices=MOVING_TYPES, max_length=32, default='DRIVING')
    tour = models.ForeignKey('PhysicalTour', on_delete=models.CASCADE)
    queue_number = models.IntegerField()


class PhysicalTour(models.Model):

    dormitory = models.ForeignKey('place.Place', on_delete=models.SET_NULL, null=True)
    food_supply = models.BooleanField(default=False)
    turoperator = models.ForeignKey('Turoperator', on_delete=models.CASCADE)
    route = models.ForeignKey('marketplace.Route', on_delete=models.CASCADE, null=True)


class CommitForPhysicalTour(models.Model):
    price = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField(null=True)
    finish_date = models.DateField(null=True)
    tour = models.ForeignKey('PhysicalTour', on_delete=models.CASCADE)
    teacher = models.ForeignKey('user.TeacherUser', on_delete=models.CASCADE, null=True)


class Turoperator(models.Model):

    name = models.CharField(max_length=32, null=True)
    logo = models.ImageField(null=True) # for demo
    documents = models.ForeignKey('documents.Document', on_delete=models.SET_NULL, null=True)
    city_zone = models.ManyToManyField('place.Place')
    user = models.ForeignKey('user.SiteUser', on_delete=models.SET_NULL, null=True)
    contact_data = models.CharField(max_length=156, null=True)