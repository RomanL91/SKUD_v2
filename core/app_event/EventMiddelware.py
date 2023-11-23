from django.http import JsonResponse

from core.utils import BaseAdapterForModels

from app_event.models import Event


# DRY по сути отличие только в типе операции


class EventMiddelware_2:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        response = self.get_response(request)
        adapter_to_controller = BaseAdapterForModels(Event, request)
        trigger = adapter_to_controller.select_message(operation_type='check_access')
        if trigger is not None:
            response = JsonResponse({})
            adapter_to_controller = BaseAdapterForModels(Event, request)
            adapter_to_controller.adapt_and_save()
        return response
    

class EventMiddelware_1:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        response = self.get_response(request)
        adapter_to_controller = BaseAdapterForModels(Event, request)
        trigger = adapter_to_controller.select_message(operation_type='events')
        if trigger is not None:
            response = JsonResponse({})
            adapter_to_controller = BaseAdapterForModels(Event, request)
            adapter_to_controller.adapt_and_save()
        return response


