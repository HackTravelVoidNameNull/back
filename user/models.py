from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .common import *

# Create your models here.


class RolePermission(models.Model):

    value = models.CharField(max_length=32)


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
    permissions = models.ManyToManyField('RolePermission')


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
    def is_admin(self):
        return self.role.name == 'admin'


class AbstractDataUser(models.Model):

    name = models.CharField(null=True, max_length=32)
    last_name = models.CharField(null=True, max_length=32)
    patronymic = models.CharField(null=True, max_length=32)
    birthdate = models.DateField(null=True, max_length=32)
    photo = models.FileField(null=True) # for demo

    class Meta:
        abstract = True


class TeacherUser(AbstractDataUser):

    position = models.CharField(max_length=32, null=True)
    user = models.ForeignKey('SiteUser', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    school = models.ForeignKey('school.School', on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField('StudentUser')


class StudentUser(AbstractDataUser):

    test_result = models.ForeignKey('marketplace.Branch', on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey('school.School', on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=32, null=True)
    user = models.ForeignKey('SiteUser', on_delete=models.CASCADE)
    parent = models.ForeignKey('ParentUser', on_delete=models.SET_NULL, null=True)


class ParentUser(AbstractDataUser):

    test_result = models.ForeignKey('marketplace.Branch', on_delete=models.SET_NULL, null=True)


class Guid(AbstractDataUser):

    type_of_teaching = models.CharField(choices=TYPE_OF_TEACHING, max_length=32, null=True)
    turoperator = models.ForeignKey('turoperator.Turoperator', on_delete=models.CASCADE, null=True)
    approved = models.BooleanField(default=False)
    accredited = models.BooleanField(default=False)


class TuroperatorIntroducer(AbstractDataUser):

    user = models.ForeignKey('SiteUser', on_delete=models.CASCADE)
    turoperator = models.ForeignKey('turoperator.Turoperator', on_delete=models.CASCADE, null=True)
