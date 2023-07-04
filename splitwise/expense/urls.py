from rest_framework import routers

from .views import GroupViewSet, ExpenseViewSet

router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'expenses', ExpenseViewSet)
urlpatterns = router.urls
