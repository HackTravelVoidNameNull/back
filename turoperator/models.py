from django.db import models

# Create your models here.
MOVING_TYPES = (
    ('DRIVING', 'На автобусе '),
    ('WALKING', 'Пешком')
)


class PhysicalTourRoute(models.Model):

    place_start = models.ForeignKey('place.Platform',
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    related_name='place_as_started')
    place_finish = models.ForeignKey('place.Platform',
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     related_name='place_as_finished')
    time_start = models.TimeField()
    time_finish = models.TimeField()
    moving_type = models.CharField(choices=MOVING_TYPES, max_length=32)
    tour = models.ForeignKey('PhysicalTour', on_delete=models.CASCADE)
    queue_number = models.IntegerField()


class PhysicalTour(models.Model):

    dormitory = models.ForeignKey('place.Place', on_delete=models.SET_NULL, null=True)
    food_supply = models.BooleanField()
    turoperator = models.ForeignKey('Turoperator', on_delete=models.CASCADE)


class CommitForPhysicalTour(models.Model):
    price = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
    tour = models.ForeignKey('PhysicalTour', on_delete=models.CASCADE)


class Turoperator(models.Model):

    name = models.CharField(max_length=32)
    documents = models.ForeignKey('documents.Document', on_delete=models.SET_NULL, null=True)
    city_zone = models.ManyToManyField('place.Place')