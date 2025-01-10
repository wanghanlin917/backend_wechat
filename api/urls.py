from rest_framework import routers
from .views.NewsInfo import NewsInfoView

router = routers.SimpleRouter(trailing_slash=False)
router.register('news', NewsInfoView, basename='news')

urlpatterns = [
]

urlpatterns += router.urls
