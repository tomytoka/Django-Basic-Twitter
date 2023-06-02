from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
import math

# posts model
class Post(models.Model):
	user = models.ForeignKey(User, related_name="posts", on_delete=models.DO_NOTHING)
	body = models.CharField(max_length=300)
	created_at=models.DateTimeField(auto_now_add=True)
	likes = models.ManyToManyField(User,related_name="post_like",blank=True)
	def number_of_likes(self):
		return self.likes.count()

	def __str__(self):
		return(
			f"{self.user}"
			f"({self.created_at:%Y-%m-%d %H:%M}): "
			f"{self.body}..."
			)
	def whenpublished(self):
		now = timezone.now()
        
		diff= now - self.created_at

		if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
			seconds= diff.seconds
            
			if seconds == 1:
				return str(seconds) +  "second ago"
            
			else:
				return str(seconds) + " seconds ago"
		
		if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
			minutes= math.floor(diff.seconds/60)

			if minutes == 1:
				return str(minutes) + " minute ago"
            
			else:
				return str(minutes) + " minutes ago"
		
		if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
			hours= math.floor(diff.seconds/3600)

			if hours == 1:
				return str(hours) + " hour ago"

			else:
				return str(hours) + " hours ago"
			
		 # 1 day to 30 days
		if diff.days >= 1 and diff.days < 30:
			days= diff.days
        
			if days == 1:
				return str(days) + " day ago"

			else:
				return str(days) + " days ago"
		if diff.days >= 30 and diff.days < 365:
			months= math.floor(diff.days/30)
            

			if months == 1:
				return str(months) + " month ago"

			else:
				return str(months) + " months ago"
		if diff.days >= 365:
			years= math.floor(diff.days/365)

			if years == 1:
				return str(years) + " year ago"

			else:
				return str(years) + " years ago"



class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	follows = models.ManyToManyField("self",related_name="followed_by",symmetrical=False,blank=True)
	date_modified = models.DateTimeField(User, auto_now=True)
	profile_image = models.ImageField(null=True,blank=True, upload_to="images/")
	
	profile_bio = models.CharField(null=True,blank=True,max_length=100)
	homepage_link =models.CharField(null=True,blank=True,max_length=100)
	instagram_link =models.CharField(null=True,blank=True,max_length=100)
	linkedin_link =models.CharField(null=True,blank=True,max_length=100)
	def __str__(self):
		return self.user.username 
	 

	
def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()
		# Have the user follow themselves
		user_profile.follows.set([instance.profile.id])
		user_profile.save()
		
post_save.connect(create_profile, sender=User)