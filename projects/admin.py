from django.contrib import admin
from projects.models.project import Project
from projects.models.issue import Issue
from projects.models.comment import Comment
from projects.models.contributor import Contributor

admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(Contributor)
