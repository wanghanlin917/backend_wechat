from rest_framework import routers
from .views.NewsInfo import NewsInfoView
from .views.login import LoginView


router = routers.SimpleRouter(trailing_slash=False)
router.register('news', NewsInfoView, basename='news')
router.register('code',LoginView,basename='code')

urlpatterns = [
]

urlpatterns += router.urls
