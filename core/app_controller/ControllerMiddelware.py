from django.http import JsonResponse

from core.utils import BaseAdapterForModels

from app_controller.models import Controller


class ControllerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        response = self.get_response(request)

        if request.body[:19] == b'csrfmiddlewaretoken':
            pass
        elif request.body:
            response = JsonResponse({})
            adapter_to_controller = BaseAdapterForModels(Controller, request)
            obj, data, created = adapter_to_controller.adapt_and_save()
            if not created:
                status_code = adapter_to_controller.send_signal(obj.ip_adress, payload=data)
                response.status_code = status_code
        return response
    