from django.urls import include, path
from rest_framework import routers
from .views import (
    FinancialDataViewSet,
    StatisticsApiView
)

router = routers.DefaultRouter()
router.register("financial_data", FinancialDataViewSet)

urlpatterns = [
    path(r"api/", include(router.urls)),
    path(r"api/statistics/", StatisticsApiView.as_view())
]
