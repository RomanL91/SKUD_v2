from django.http import JsonResponse

from core.utils import BaseAdapterForModels

from app_controller.models import Controller


class ControllerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        print(" -------->>> custom middleware before next middleware/view")
        response = self.get_response(request)

        if request.body[:19] == b'csrfmiddlewaretoken':
            pass
        elif request.body:
            adapter_to_controller = BaseAdapterForModels(Controller, request)
            adapter_to_controller.adapt_and_save()
            response = JsonResponse({})
        print(response.status_code)
        return response
