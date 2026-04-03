from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 1. 定义白名单：这些路径不需要登录就能访问
        # 注意：这里要包含登录页面本身，否则会重定向死循环
        white_list = ['/login/', '/register/', '/static/']
        if request.path_info in white_list:
            return

        # 2. 读取 Session
        info = request.session.get('info')

        # 3. 如果 Session 存在（已登录），放行
        if info:
            return

        # 4. 如果没登录，重定向到登录页面
        return redirect('/login/')