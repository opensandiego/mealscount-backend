# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

state_or_province_choices = (
    ("AL", "Alabama"),
    ("AK", "Alaska"),
    ("AZ", "Arizona"),
    ("AR", "Arkansas"),
    ("CA", "California"),
    ("CO", "Colorado"),
    ("CT", "Connecticut"),
    ("DE", "Delaware"),
    ("DC", "District of Columbia"),
    ("FL", "Florida"),
    ("GA", "Georgia"),
    ("HI", "Hawaii"),
    ("ID", "Idaho"),
    ("IL", "Illinois"),
    ("IN", "Indiana"),
    ("IA", "Iowa"),
    ("KS", "Kansas"),
    ("KY", "Kentucky"),
    ("LA", "Louisiana"),
    ("ME", "Maine"),
    ("MD", "Maryland"),
    ("MA", "Massachusetts"),
    ("MI", "Michigan"),
    ("MN", "Minnesota"),
    ("MS", "Mississippi"),
    ("MO", "Missouri"),
    ("MT", "Montana"),
    ("NE", "Nebraska"),
    ("NV", "Nevada"),
    ("NH", "New Hampshire"),
    ("NJ", "New Jersey"),
    ("NM", "New Mexico"),
    ("NY", "New York"),
    ("NC", "North Carolina"),
    ("ND", "North Dakota"),
    ("OH", "Ohio"),
    ("OK", "Oklahoma"),
    ("OR", "Oregon"),
    ("PA", "Pennsylvania"),
    ("PR", "Puerto Rico"),
    ("RI", "Rhode Island"),
    ("SC", "South Carolina"),
    ("SD", "South Dakota"),
    ("TN", "Tennessee"),
    ("TX", "Texas"),
    ("UT", "Utah"),
    ("VT", "Vermont"),
    ("VA", "Virginia"),
    ("WA", "Washington"),
    ("WV", "West Virginia"),
    ("WI", "Wisconsin"),
    ("WY", "Wyoming"),
)
# Models for MealsCount Backend

# Model for a MealsCount Response

class MC_RESULT(models.Model):
    json_string = models.CharField(max_length=10000)


# Model for a MealsCount Request

class MC_REQUEST(models.Model):
    request_time = models.DateTimeField()
    pending = models.BooleanField()
    email = models.CharField(max_length=100)
    result = models.ForeignKey(MC_RESULT, on_delete=models.PROTECT, null=True)


def define_path(instance, filename):
    return 'district_data/{}/{}'.format(instance.district_name, filename)


class District(models.Model):
    district_name = models.CharField(max_length=200)
    district_data_file = models.FileField(upload_to=define_path)
    state_or_province = models.CharField(
        max_length=2,
        choices=state_or_province_choices,
        default="CA",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # TODO: Add users to District
    # who_uploaded = models.OneToOneField(User, on_delete=models.PROTECT)

    class META:
        verbose_name = "District"
        verbose_name_plural = "Districts"



class DistrictAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    district = models.ForeignKey(District, on_delete=models.PROTECT)

    class META:
        verbose_name = "Admin"
        verbose_name_plural = "Admins"



class School(models.Model):
    school_name = models.CharField(max_length=200)
    total_number_of_students = models.IntegerField()
    identified_student_population = models.IntegerField()
    # request = models.ForeignKey(MC_REQUEST, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT)

    class META:
        verbose_name = "School"
        verbose_name_plural = "Schools"


# Jlangley: not sure about these 2 methods create_user_profile and save_user_profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        DistrictAdmin.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.districtadmin.save()
