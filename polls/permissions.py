from rest_framework.permissions import BasePermission, SAFE_METHODS

from datetime import date


class PollPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        today = date.today()
        view.queryset = view.queryset.filter(start_date__lte=today, finish_date__gte=today)

        return request.method.upper() in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return request.method.upper() in SAFE_METHODS


class QuestionPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        return request.method.upper() in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return request.method.upper() in SAFE_METHODS


class AnswerGatewayPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.user.is_authenticated:
            view.queryset = view.queryset.filter(user=request.user)
        else:
            view.queryset = view.queryset.none()

        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return request.method.upper() in SAFE_METHODS