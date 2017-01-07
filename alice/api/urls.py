from django.conf.urls import url, include

from rest_framework import routers

from .views import (
    AnalysisView,
    VectorizerView,
    PredictorView,
)

router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = [
    url(r'^v1/ana', AnalysisView.as_view()),
    url(r'^v1/vec$', VectorizerView.as_view()),
    url(r'^v1/pre', PredictorView.as_view()),
]


