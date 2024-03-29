"""Softdesk_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from projects.views.projectviewset import ProjectViewset
from projects.views.issueviewset import IssueViewset
from projects.views.commentviewset import CommentViewset
from projects.views.contributorviewset import ContributorViewset

router = routers.SimpleRouter()
router.register('projects',
                ProjectViewset,
                basename='projects')
router.register(r'projects/(?P<project_id>\d+)/issues',
                IssueViewset,
                basename='issues')
router.register(r'projects/(?P<project_id>\d+)/issues/('
                r'?P<issue_id>\d+)/comments',
                CommentViewset,
                basename='comments')
router.register(r'projects/(?P<project_id>\d+)/users',
                ContributorViewset,
                basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('', include(router.urls))
]
