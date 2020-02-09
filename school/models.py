from django.db import models
# Create your models here.


class School(models.Model):

    name = models.CharField(max_length=32)
    address = models.ForeignKey('place.Place', on_delete=models.SET_NULL, null=True)
    documents = models.ForeignKey('documents.Document', on_delete=models.SET_NULL, null=True)
    score = models.IntegerField(default=0)

    def __repr__(self):
        return '{} {}'.format(self.name, self.address.short_address)

