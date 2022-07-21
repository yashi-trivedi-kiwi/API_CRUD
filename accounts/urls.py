from django.urls import path, include
from rest_framework import routers


from accounts.views import UserView

router = routers.DefaultRouter()
router.register('user-account', UserView, basename='user_account')

urlpatterns = [
    path('account', include(router.urls)),
]
