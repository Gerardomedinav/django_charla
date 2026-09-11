from django.urls import path
from .views import dashboard_views, docs_views

app_name = 'core'

urlpatterns = [
    path('', dashboard_views.dashboard, name='dashboard'),
    path('swagger/', docs_views.swagger_ui, name='swagger_ui'),
    path('redoc/', docs_views.redoc_ui, name='redoc_ui'),
    path('api/docs/', docs_views.swagger_ui, name='api_docs'),
    path('api/schema.json', docs_views.openapi_schema, name='openapi_schema'),
]
