from django.db import models

# Create your models here.

MONTHS = (  
    ('4', 'April'),
    ('5', 'May'),
    ('6', 'June'),
    ('7', 'July'),
    ('8', 'August'),
    ('9', 'September'),
   )

MONTHS_DICT = dict(MONTHS)

class Input(models.Model):
    month = models.CharField(max_length=2, choices=MONTHS)
    name  = models.CharField(max_length=50)
