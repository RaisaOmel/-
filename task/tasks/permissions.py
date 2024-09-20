from rest_framework import permissions

class IsAuther(permissions.BasePermission):

    # def has_permission(self, request, view):
    #     return request.auth == request.user

    #отбор задачи данного пользователя
    def has_object_permission(self, request, view,obj):
        return obj.user == request.user