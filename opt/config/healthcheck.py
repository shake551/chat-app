from django.http import JsonResponse


def healthcheck(request):
    return JsonResponse({'message': 'ok'}, status=200)
