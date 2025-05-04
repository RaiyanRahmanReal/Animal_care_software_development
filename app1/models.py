from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Petadd(models.Model):
    name = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    age = models.IntegerField()
    identifying_marks = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_pets')
    image = models.ImageField(upload_to='pets/')
    sold = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_for_adoption = models.BooleanField(default=False)

    buyer = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='bought_pets')
    adopter = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='adopted_pets')

    def __str__(self):
        return self.name

    def is_owner(self, user):
        return self.owner == user


# Daycare request model
class DaycareRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet_name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    identifying_marks = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    accepted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='accepted_requests')
    pet_photo = models.ImageField(upload_to='daycare_pets/', null=True, blank=True)

    def __str__(self):

        return f"{self.pet_name} ({self.user.username})"

    def is_owner(self, user):
        """Check if the given user is the owner of this daycare request pet."""
        return self.user == user

    def clean(self):
        """Ensure that a daycare request can only be approved or rejected, not both."""
        if self.approved and self.rejected:
            raise ValidationError("A request cannot be both approved and rejected.")
       

    def save(self, *args, **kwargs):
        """Override save method to ensure only one of approved or rejected is set."""
        self.clean()  
        super().save(*args, **kwargs)

