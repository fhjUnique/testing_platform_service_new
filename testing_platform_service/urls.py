"""testing_platform_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from testing_platform_service.apps.api_public import view as api_public
from testing_platform_service.apps.api_role_manage import view as api_role_manage
from testing_platform_service.apps.api_users_manage import view as api_users_manage
from testing_platform_service.apps.api_project_manage import view as api_project_manage

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login', api_public.api_login),
    # 角色管理
    path('getUserPermission', api_role_manage.api_get_user_permission),
    path('getPermission', api_role_manage.api_get_permission),
    path('addRole', api_role_manage.api_add_role),
    path('updateRole', api_role_manage.api_update_role),
    path('deleteRole', api_role_manage.api_delete_role),
    path('getRole', api_role_manage.api_get_role_list),
    path('getRoleDetail', api_role_manage.api_get_role_detail),
    path('addPermission', api_role_manage.api_add_permission),
    path('updatePermission', api_role_manage.api_update_permission),
    path('deletePermission', api_role_manage.api_delete_permission),
    # 用户管理
    path('addUserInfo', api_users_manage.api_add_user),
    path('updateUserInfo', api_users_manage.api_update_user),
    path('activeUserInfo', api_users_manage.api_operation_user),
    path('deleteUserInfo', api_users_manage.api_delete_user),
    path('getUserInfo', api_users_manage.api_get_user),
    # 项目管理
    path('getProject', api_project_manage.api_get_project),
    path('addProject', api_project_manage.api_add_project),
    path('updateProject', api_project_manage.api_update_project),
    path('deleteProject', api_project_manage.api_delete_project),

]
