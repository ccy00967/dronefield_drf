from rest_framework import permissions

class OnlyOwnerCanUpdate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 만약 그냥 일반 사용자 - GET, HEAD, OPTIONS 요청에만 True - 3개를 안전한 요청이라고 한다
        if request.method in permissions.SAFE_METHODS:
            return True
        # 만약 위의 3개중 하나가 아닌 경우 request.user가 obj.owner와 동일할때만 가능
        return obj.email == request.user.email
        
