from django.db import models

class Company(models.Model):
    """
    This model represent the Company of the user.
    """
    
    name = models.CharField(max_length=100,null=False, blank=False)
    address = models.CharField(max_length=100,null=False, blank=False)
    siret = models.CharField(max_length=14,null=False, blank=False)

    def __str__(self):
        return self.company