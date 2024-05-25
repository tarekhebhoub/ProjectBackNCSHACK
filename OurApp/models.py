from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.

class User(AbstractUser):
    Date_Of_Birth = models.DateField(blank=True, null=True)
    Specialite = models.CharField(max_length=25, null=True)
    is_client = models.BooleanField(default=False)
    groups = models.ManyToManyField('auth.Group', related_name='client_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='client_user_permissions')

# class Rapport(models.Model):
#     # client = models.ForeignKey(User, on_delete=models.CASCADE)
#     rapport = models.ForeignKey(Rapport,on_delete=models.CASCADE)
#     # created_at = models.DateTimeField(default=timezone.now)

class RendezVous(models.Model):
    medecin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medecin_rendezvous')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_rendezvous')
    pourcentage = models.IntegerField()
    # rapport = models.ForeignKey(Rapport, on_delete=models.CASCADE, null=True)
    class Meta:
        unique_together = ('client', 'medecin')

class MesPatiens(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_mespations')
    medecin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medecin_mespations')
    rapport = models.ForeignKey('Room', on_delete=models.CASCADE)
    date = models.DateField()
    class Meta:
        unique_together = ('client', 'medecin', 'rapport')

class DemmandAllRapports(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_demmandallrapports')
    medecin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medecin_demmandallrapports')
    canGetAllR = models.BooleanField(default=False)
    class Meta:
        unique_together = ('client', 'medecin')



class Room(models.Model):
	client=models.ForeignKey(User,on_delete=models.CASCADE)
    #created_at=models.DateTimeField(default=timezone.now)
    
class Message(models.Model):
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	question=models.CharField(max_length=255)
	timestamp = models.DateTimeField(auto_now_add=True)
	reponse=models.CharField(max_length=255)
	def __str__(self):
		return self.content
