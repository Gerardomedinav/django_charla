"""
Vistas de Documentación OpenAPI, Swagger UI y ReDoc.
"""

from django.shortcuts import render
from django.http import JsonResponse
from core.openapi import OPENAPI_SPEC

def openapi_schema(request):
    """
    Especificación OpenAPI 3.0.3 en formato JSON para Swagger UI, ReDoc, Postman e Insomnia.
    """
    return JsonResponse(OPENAPI_SPEC)

def swagger_ui(request):
    """
    Interfaz interactiva de Swagger UI para pruebas de QA, Frontend y documentación viva.
    """
    return render(request, 'restaurante/swagger.html')

def redoc_ui(request):
    """
    Documentación viva en formato ReDoc de 3 paneles.
    """
    return render(request, 'restaurante/redoc.html')
