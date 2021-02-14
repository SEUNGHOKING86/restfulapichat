from django.conf.urls import url, include
#from addresses import views
from django.urls import path
from django.contrib import admin

urlpatterns = [
 #    path('addresses/', views.address_list),
 #    path('addresses/<int:pk>/', views.address),
 #    path('login/', views.login),
 # #   path('chathome/', views.home),
 #    path('app_login/', views.app_login),
    path('admin/', admin.site.urls),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url('^$', views.login_page),
    path('', include('addresses.urls')),
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
     ]
}

