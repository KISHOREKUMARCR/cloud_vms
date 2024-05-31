from django.urls import path
from accounts import views
# from django.conf.urls import url
# from django.urls import include, re_path,path
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('index', views.index, name = 'index'),
    path('logout', LogoutView.as_view(), name="logout"),
    path('', views.loginprocess, name = 'loginprocess'),
    
    path('profile', views.profile_view_final, name='profile_view_final'),
    path('upload', views.upload, name='upload'),
    path('account_delete', views.profile_edit_account_delete, name='profile_edit_account_delete'),
    path('account_security', views.profile_edit_security, name='profile_edit_security'),
    path('edit_profile', views.profile_edit_final, name='profile_edit_final'),
    #path('profile', views.view_profile, name='view_profile'),
    #path('profile/<pk>/', views.view_profile, name='view_profile_with_pk'),
    #path('edit_profile', views.edit_profile_account, name='edit_profile_account'),
    #path('edit_profile/<pk>/', views.edit_profile_account, name='edit_profile_account_with_pk'),
    path('terms_conditions',views.terms_conditions, name = 'terms_conditions'),
    #path('social_login_google', views.social_login_google, name = 'social_login_google'),
    path('load_timer', views.load_timer, name = 'load_timer'),
    path('login_account_google', views.login_account_google, name = 'login_account_google'),
    path('camera_list_update', views.camera_list_update, name ='camera_list_update'),
    #path('validate_login', views.validate_login.as_view(), name = "validate_login"),
    path("logout_request", views.logout_request, name= "logout_request"),
    path('registration', views.registration, name = 'registration'),
    #path('vali_register', views.vali_register, name = 'register'),
    path('validate_username', views.validate_username, name='validate_username'),   
    # url(r'^validate_username/$', views.validate_username, name='validate_username'),
    #url(r'^validate_login_user/$', views.validate_login_user, name='validate_login_user'),
    #url(r'^validate_login/$', views.validate_login, name='validate_login'),
    #url(r'^vali_register/$', views.vali_register, name='vali_register'),
	path('reset/<uidb64>/<token>/', views.auth_password_confirm,name='auth_password_confirm'),
	path('auth_forget_password', views.auth_forget_password, name = 'auth_forget_password'),
	path('forget_username', views.forget_username, name = 'forget_username'),
	path('auth_forget_password_msg', views.auth_forget_password_msg, name = 'auth_forget_password_msg'),
	path('forget_username_msg', views.forget_username_msg, name = 'forget_username_msg'),
    # path('auth_superadmin', views.auth_superadmin, name = 'auth_superadmin'),
    path('auth_admin', views.auth_admin, name = 'auth_admin'),
    path('auth_user', views.auth_user, name = 'auth_user'),
    path('super_admin', views.super_admin_view, name = 'super_admin'),
    path('role_auth', views.role_based_auth, name = 'role_auth'),
    path('delete_user', views.DeleteUser.as_view(), name = 'delete_user'),
    path('update_auth_form/<str:pk>/', views.update_auth_form, name = 'update_auth_form'),
    path('update_role', views.UpdateRoles.as_view(), name = 'update_role'),
    # Role Data Table CRUD
    path('delete_role_table', views.DeleteRoleDataTable.as_view(), name = "delete_role_table"),
    path('add_role_table', views.AddRoleDataTable.as_view(), name = "add_role_table"),
    path('get_role_table', views.GetRoleData.as_view(), name = "get_role_table"),
    path('update_role_table', views.UpdateRoleData.as_view(), name = "update_role_data"),
    path('role_table_view', views.role_data_table_view, name = "role_table_view"),
    # User Account Table CRUD
    path('user_table_view', views.user_table_view, name = "user_table_view"),
    path('user_data_table', views.UserDataTable.as_view(), name = "user_data_table"),
    # kvs streams
    # path('kvs_view', views.kvs_view, name = "kvs_view"),
    # path('create_kvs_data', views.CreateKvsData.as_view(), name = 'create_kvs_data'),
    # path('update_kvs_data', views.UpdateKvsData.as_view(), name = "update_kvs_data"),
    # path('delete_kvs_data', views.DeleteKvsData.as_view(), name = 'delete_kvs_data'),
    path('role_data_table', views.RolesDataTable.as_view(), name = "role_data_table"),
    
]
