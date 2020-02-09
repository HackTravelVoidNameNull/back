from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .common import *

# Create your models here.

SYSTEM_ROLES = (
    ('teacher', 'teacher'),
    ('student', 'student'),
    ('guid', 'guid'),
    ('turoperator', 'turoperator'),
    ('parent', 'parent'),
    ('admin', 'tester or admin')
)


class SystemRole(models.Model):

    name = models.CharField(max_length=32, choices=SYSTEM_ROLES)


class SiteUserManager(BaseUserManager):

    def _create_user(self, phone_number, email, password, **kwargs):
        if not phone_number:
            raise ValueError('The given phone number must be set')
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        kwarg = {'role':SystemRole.objects.get_or_create(name='admin')}
        return self._create_user(username, email, password, **kwarg)


class SiteUser(AbstractBaseUser):

    USERNAME_FIELD = 'phone_number'

    EMAIL_FILED = 'email'
    REQUIRED_FIELDS = ['password', 'email']

    email = models.EmailField(max_length=64, unique=True)
    phone_number = models.CharField(max_length=32, unique=True)
    role = models.ForeignKey('SystemRole', on_delete=models.SET_NULL, null=True)

    @property
    def is_teacher(self):
        return self.role.name == 'teacher'

    @property
    def is_parent(self):
        return self.role.name == 'parent'

    @property
    def is_turoperator(self):
        return self.role.name == 'turoperator'

    @property
    def is_guid(self):
        return self.role.name == 'guid'

    @property
    def is_student(self):
        return self.role.name == 'student'

    @property
    def is_tester(self):
        return self.role.name == 'tester'


class AbstractDataUser(models.Model):

    name = models.CharField(null=True, max_length=32)
    last_name = models.CharField(null=True, max_length=32)
    patronymic = models.CharField(null=True, max_length=32)
    birthdate = models.DateField(null=True, max_length=32)
    photo = models.FileField(null=True) # for demo

    class Meta:
        abstract = True


class TeacherUser(AbstractDataUser):

    chosen_branches = models.ManyToManyField('marketplace.Branch')
    position = models.CharField(max_length=32, null=True)
    user = models.ForeignKey('SiteUser', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    school = models.ForeignKey('school.School', on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField('StudentUser')


class StudentUser(AbstractDataUser):

    chosen_branches = models.ManyToManyField('marketplace.Branch')
    school = models.ForeignKey('school.School', on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=32, null=True)
    user = models.ForeignKey('SiteUser', on_delete=models.CASCADE)
    parent = models.ForeignKey('ParentUser', on_delete=models.SET_NULL, null=True)
    tours = models.ManyToManyField


class ParentUser(AbstractDataUser):

    test_result = models.ForeignKey('marketplace.Branch', on_delete=models.SET_NULL, null=True)


class Guid(AbstractDataUser):

    type_of_teaching = models.CharField(choices=TYPE_OF_TEACHING, max_length=32, null=True)
    turoperator = models.ForeignKey('turoperator.Turoperator', on_delete=models.CASCADE, null=True)
    approved = models.BooleanField(default=False)
    accredited = models.BooleanField(default=False)
    tours = models.ManyToManyField('turoperator.CommitForPhysicalTour')


class TuroperatorIntroducer(AbstractDataUser):

    user = models.ForeignKey('SiteUser', on_delete=models.CASCADE, null=True)
    turoperator = models.ForeignKey('turoperator.Turoperator', on_delete=models.CASCADE, null=True)
