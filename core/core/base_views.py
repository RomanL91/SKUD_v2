from django.shortcuts import redirect

from django.views.decorators.csrf import csrf_exempt

from core.BaseAdapter import BaseAdapterForModels


@csrf_exempt
def controller_request_receiver_gateway(request):

    if request.method == "GET":
        return redirect(to='/admin/')   #HARDCODE

    adapter = BaseAdapterForModels(request_adaptee=request)    

    adapter.get_input_data()
    return adapter.adapt_and_save_2()
