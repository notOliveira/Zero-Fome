from django.db import models
from PIL import Image
from .constants import STATE_CHOICES

class Organization(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    cep = models.CharField(max_length=9, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    neighborhood = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, blank=True, null=True)
    number = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField('users.CustomUser', related_name='organization_users', blank=True)
    # Work on category system in the future
    # category = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name

class OrganizationProfile(models.Model):
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
    image = models.ImageField(default='default_org_picture.png', upload_to='org_pics')
    website = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.organization.name} - Profile'
    
    # Substituindo método save
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)