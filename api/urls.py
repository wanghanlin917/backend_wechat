from rest_framework import routers
from .views.NewsInfo import NewsInfoView
from .views.login import SmsCodeView,LoginView

router = routers.SimpleRouter(trailing_slash=False)
router.register('news', NewsInfoView, basename='news')
router.register('code',SmsCodeView,basename='code')
router.register('login',LoginView,basename='login')

urlpatterns = [
]

urlpatterns += router.urls
