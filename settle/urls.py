from rest_framework  import routers
from .views import SettleViewSet

router = routers.DefaultRouter()

router.register(r'settle', SettleViewSet, basename='settle')
urlpatterns = router.urls