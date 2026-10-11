from django.db import connection
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def healthz(request):
    return JsonResponse({'status':'ok'})


@require_GET
def readiness(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
        cursor.fetchone()
    return JsonResponse({'status':'ok','database':connection.vendor})
