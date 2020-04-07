from django.db import models

from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):

    title = models.CharField(max_length = 200)
    slug = models.SlugField(unique = True)
    description = models.TextField(max_length = 500)
    
    def __str__(self):
        return ( '%s' % (self.title) )


class Post(models.Model):
    text = models.TextField()
    url = models.URLField()
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_posts")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_posts", blank=True, null=True)