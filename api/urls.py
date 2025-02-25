from rest_framework import routers
from .views.NewsInfo import NewsInfoView, AddHouseInfoView,WarrantyView,RepairProjectView
from .views.login import SmsCodeView, LoginView, UserInfoView

router = routers.SimpleRouter(trailing_slash=False)
router.register('news', NewsInfoView, basename='news')
router.register('code', SmsCodeView, basename='code')
router.register('login', LoginView, basename='login')
router.register('userInfo', UserInfoView, basename='userInfo')
router.register('room', AddHouseInfoView, basename='room')
router.register('house', WarrantyView, basename='house')
router.register('repairItem',RepairProjectView,basename='repairItem')

urlpatterns = [
]

urlpatterns += router.urls
