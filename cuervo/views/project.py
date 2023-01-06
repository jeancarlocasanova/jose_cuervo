from django.views.generic import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from cuervo.models import Project

class ProjectListView(ListView):
    def get_queryset(self):
        qs = Project.objects.all()
        return qs
