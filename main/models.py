from django.db import models


from user.models import CustomUser


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # This field is used for possible map integration
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # This field is used for possible map integration
    image = models.ImageField(upload_to='loc_pics/')
    working_hours = models.JSONField(default=dict, blank=True)
    description = models.TextField(blank=True, null=True)
    views = models.ManyToManyField(CustomUser, blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='comments')
    likes = models.ManyToManyField(CustomUser)
    parent_comment = models.ForeignKey(to='Comment', on_delete=models.CASCADE, blank=True,
                                       null=True,
                                       related_name='replied_comments')  # User is able to reply to comments.
    created_at = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, related_name='ratings', on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField()  # 1 to 5 stars
