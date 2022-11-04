"""
class through Contributor

@author : Sylvain GAUTHIER
@version : 1.0
"""


from django.db import models
from django.conf import settings

PERMISSIONS = (
    ('author', 'Auteur'),
    ('contributor', 'Contributeur')
)

ROLES = (
    ('author', 'Auteur'),
    ('contributor', 'Contributeur')
)


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
