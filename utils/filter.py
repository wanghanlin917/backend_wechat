from rest_framework.filters import BaseFilterBackend


class MineFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # print("认证输出", request.user, request.auth)
        if not request.user:
            return queryset
        user_id = request.user.get('user_id')
        if user_id:
            return queryset.filter(id=user_id)
        return queryset
