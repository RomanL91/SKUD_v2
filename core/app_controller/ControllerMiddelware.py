from django.http import JsonResponse

from core.utils import BaseAdapterForModels

from app_controller.models import Controller


class ControllerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        response = self.get_response(request)
        adapter_to_controller = BaseAdapterForModels(Controller, request)
        trigger = adapter_to_controller.select_message(operation_type='power_on')
        if trigger is not None:

            response = JsonResponse({})
            obj, data, created = adapter_to_controller.adapt_and_save()
            if not created:
                status_code = adapter_to_controller.send_signal(obj.ip_adress, payload=data)
                response.status_code = status_code
        return response
    