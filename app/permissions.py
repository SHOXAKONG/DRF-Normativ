# from rest_framework.exceptions import PermissionDenied
# from rest_framework.permissions import BasePermission
#
#
# class IsOwnerOrReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         if request.method == "POST":
#             project_id = request.data.get('project')
#             if not project_id:
#                 raise PermissionDenied("Need Project ID")
#             from .models import Projects
#             project = Projects.objects.filter(id=project_id).first()
#             if not project or project.owner != request.user:
#                 raise PermissionDenied("Owner Can only create Task")
#         return True
