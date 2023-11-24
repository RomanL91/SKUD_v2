from django.shortcuts import redirect

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from core.utils import BaseAdapterForModels

from django.utils import timezone


@csrf_exempt
def controller_request_receiver_gateway(request):

    if request.method == "GET":
        return redirect(to='/admin/')   #HARDCODE

    adapter = BaseAdapterForModels(request_adaptee=request)    

    try:
        req_to_json, operition_type = adapter.to_json()
    except TypeError as e:
        resp = JsonResponse(data={'TypeError': str(e)})
        resp.status_code = 400
        return resp
    
    if req_to_json is not None:
        print(f'======== Тип операции {operition_type} ======== {timezone.now()}')
        adapter.operition_type = operition_type
        return adapter.adapt_and_save()
