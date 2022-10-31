"""
class Project

@author : Sylvain GAUTHIER
@version : 1.0
"""


from django.db import models
from django.conf import settings

TYPES = (
    ('BACKEND', 'back-end'),
    ('FRONTEND', 'front-end'),
    ('IOS', 'iOS'),
    ('ANDROID', 'Android')
)


class Project(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2048)
    type = models.CharField(max_length=30,
                            choices=TYPES)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE,
                                       null=True)
