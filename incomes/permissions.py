from rest_framework import permissions
import datetime


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsVerified(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        num_of_days = str(datetime.date.today() -
                          obj.owner.created_at.date()).split(' ')
        num_of_days = int(num_of_days[0])
        return (obj.owner.is_verified or (num_of_days < 30))
