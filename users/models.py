from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils import timezone
from PIL import Image

# from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(default="Anonymous", max_length=30)
    last_name = models.CharField(default="User", max_length=30)
    bio = models.CharField(max_length=1000, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    image = models.ImageField(default="default.png", upload_to="profile.pic/")
    country = CountryField(blank=True)  # Add country field
    date_of_birth = models.DateField(
        default="2000-01-01", blank=True
    )  # Add date of birth field
    date_of_joining = models.DateField(
        default=timezone.now()
    )  # Add date of joining field with today's date by default and non-changeable
    instagram = models.URLField(max_length=255, blank=True)  # Add Instagram field
    linkedin = models.URLField(max_length=255, blank=True)  # Add LinkedIn field
    github = models.URLField(max_length=255, blank=True)  # Add GitHub field
    facebook = models.URLField(max_length=255, blank=True)  # Add GitHub field
    twitter = models.URLField(max_length=255, blank=True)  # Add GitHub field

    def __str__(self) -> str:
        return f"{self.user.username} - Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
