from django.db import models, transaction
from django.conf import settings

TYPES = (
    ('BACKEND', 'back-end'),
    ('FRONTEND', 'front-end'),
    ('IOS', 'iOS'),
    ('ANDROID', 'Android')
)

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

PERMISSIONS = (
    ('author', 'Auteur'),
    ('contributor', 'Contributeur')
)

ROLES = (
    ('author', 'Auteur'),
    ('contributor', 'Contributeur')
)


class Project(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2048)
    type = models.CharField(max_length=30,
                            choices=TYPES)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE,
                                       null=True)


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


class Comment(models.Model):

    description = models.CharField(max_length=2048)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE)
    issue_id = models.ForeignKey('projects.Issue',
                                 on_delete=models.CASCADE,
                                 related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)


class Contributor(models.Model):

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    project_id = models.ForeignKey('projects.Project',
                                   on_delete=models.CASCADE,
                                   related_name='contributors')
    permission = models.CharField(max_length=255,
                                  choices=PERMISSIONS)
    role = models.CharField(max_length=255,
                            choices=ROLES)
