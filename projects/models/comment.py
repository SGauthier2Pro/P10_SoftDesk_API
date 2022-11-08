"""
class Comment

@author : Sylvain GAUTHIER
@version : 1.0
"""


from django.db import models
from django.conf import settings


class Comment(models.Model):

    description = models.CharField(max_length=2048)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE)
    issue_id = models.ForeignKey('projects.Issue',
                                 on_delete=models.CASCADE,
                                 related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)
