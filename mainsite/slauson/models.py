from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return "%s' profile" % self.user

    '''def save(self, *args, **kwargs):
        self.slug = (slugify(self.location))
        super(Profile, self).save(*args, **kwargs)'''

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        profile = Profile(user=user)
        profile.save()


post_save.connect(create_profile, sender=User)