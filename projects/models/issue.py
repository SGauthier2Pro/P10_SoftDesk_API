from django.db import models
from django.conf import settings

TAGS = (
    ('BUG', 'BUG'),
    ('ENHANCEMENT', 'AMÉLIORATION'),
    ('TASK', 'TÂCHE')
)

PRIORITIES = (
    ('low', 'FAIBLE'),
    ('medium', 'MOYENNE'),
    ('high', 'ÉLEVÉE')
)

STATUS = (
    ('todo', 'À faire'),
    ('inprogress', 'En cours'),
    ('terminated', 'Terminé')
)


class Issue(models.Model):

    title = models.CharField(max_length=255)
    desc = models.TextField(max_length=2048)
    tag = models.CharField(max_length=30,
                           choices=TAGS)
    priority = models.CharField(max_length=30,
                                choices=PRIORITIES)
    project_id = models.ForeignKey('projects.Project',
                                   on_delete=models.CASCADE,
                                   related_name='issues')
    status = models.CharField(max_length=30,
                              choices=STATUS)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE,
                                       related_name='author')
    assignee_user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                         on_delete=models.CASCADE,
                                         related_name='assignee_user_id',
                                         null=True)
    created_time = models.DateTimeField(auto_now_add=True)