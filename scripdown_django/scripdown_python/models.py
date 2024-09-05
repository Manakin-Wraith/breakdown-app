from django.db import models
from django.contrib.auth.models import User

class Script(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Character(models.Model):
    script = models.ForeignKey(Script, on_delete=models.CASCADE, related_name='characters')
    name = models.CharField(max_length=100)
    importance = models.CharField(max_length=20, choices=[
        ('lead', 'Lead'),
        ('supporting', 'Supporting'),
        ('minor', 'Minor'),
    ])

class Scene(models.Model):
    script = models.ForeignKey(Script, on_delete=models.CASCADE, related_name='scenes')
    number = models.IntegerField()
    location = models.CharField(max_length=200)
    description = models.TextField()

class Element(models.Model):
    script = models.ForeignKey(Script, on_delete=models.CASCADE, related_name='elements')
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name='elements')
    category = models.CharField(max_length=50, choices=[
        ('prop', 'Prop'),
        ('costume', 'Costume'),
        ('special_effect', 'Special Effect'),
        ('stunt', 'Stunt'),
        ('vehicle', 'Vehicle'),
        ('animal', 'Animal'),
        ('vfx', 'VFX'),
    ])
    description = models.CharField(max_length=200)

class Budget(models.Model):
    script = models.OneToOneField(Script, on_delete=models.CASCADE, related_name='budget')
    total_estimate = models.DecimalField(max_digits=10, decimal_places=2)
    breakdown = models.JSONField()  # Store detailed budget breakdown as JSON
