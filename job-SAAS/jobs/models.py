from django.db import models

class LLMResult(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('processing','Processing'),
        ('ready','Ready')
    ]

    title = models.CharField(max_length=256)
    prompt = models.TextField()
    

# Create your models here.


class JoblistingResult(models.Model):
    pass

class snapshot(models.Model):
    pass