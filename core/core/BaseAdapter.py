import json, requests
from pprint import pprint
from datetime import datetime

from django.http import JsonResponse

from django.utils import timezone
from django.db import models
from django.db.models import Q

from app_controller.models import Controller
from app_event.models import Event
from app_card_pass.models import CardPass

from core.ServicesMultiProc import MultiprocessingDecorator


class BaseAdapterForModels:
    payload = None
    obj_staff = None
    event_staff = 'Не известный'
    event_checkpoint = 'Не известная проходная'
    event_direction = 'Не известно направление'
    granted_0 = [2, 4, 6, 7, 14, 17, 26, 28, 30]
    event_serial_num_controller = None
    event = None

#  Нужно подумать о приватности и гетарах сетерах
    __controller: models = Controller
    __event: models = Event
    __card_pass: models = CardPass

    __header_resonse: dict = {"date": None, "interval": 10, "sn": None, "messages": None,}
    set_mode: dict = {"id": 1, "operation": "set_mode", "mode": None}
    set_active: dict = {"id": 0, "operation": "set_active", "active": None, "online": None}
    add_card: dict = {
        "id": 0, "operation": "add_cards", "cards": [
            {"card": None, "flags": 0, "tz": 255},]}
    del_card: dict = {"id": 0,  "operation": "del_cards", "cards": [
                {"card": None},]}
    __granted = {"id": 0, "operation": "check_access", "granted": None}
    __resp_event = {"id":0, "operation": "events", "events_success": None}

    __late_status = 'Без нарушений графика'
    __late = False
    __queue_broken = False

    schedule_for_today = None
    week_days = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье')
  

    def __init__(self, request_adaptee=None, operition_type=None) -> None:
        self.request_adaptee = request_adaptee
        self.operition_type = operition_type

    
    def get_input_data(self):
        if b'messages' in self.request_adaptee.body:
            self.data_request = json.loads(self.request_adaptee.body)
            self.message_package = self.data_request['messages']


    def adapt_and_save_2(self):
        print(f'[==INFO==] start -----------------------{timezone.now()}-----------------------')
        message_reply = []
        count = 0
        for messege in self.message_package:    #перебираю сообщения от контроллера
            print(f'[==INFO==] received msg: <<-- {messege}')
            try:                                #пытаюсь получить ключ operation из словаря
                operations_type = messege['operation']
                if operations_type == 'power_on':
                    print('[==INFO==] power_on')
                    obj, create = self.__controller.objects.get_or_create(
                        type_controller = self.data_request['type'],
                        serial_number = self.data_request['sn']
                    )
                    if create:
                        continue
                    else:
                        self.set_active['active'] = int(obj.controller_activity)
                        self.set_active['online'] = int(obj.controller_online.split('/')[0])
                        self.set_mode['mode'] = int(obj.controller_online.split('/')[1])
                        message_reply.extend([self.set_active, self.set_mode])
                        self.payload = self.response_model(message_reply, obj.serial_number) #??? self.message_package
                        continue
                elif operations_type == 'events':
                    print('[==INFO==] events')
                    events = messege[operations_type]
                    count = len(events)
                    self.__resp_event['events_success'] = count
                    message_reply.append(self.__resp_event)
                    continue
                elif operations_type == 'ping':
                    print('[==INFO==] ping')
                    continue
                elif operations_type == 'check_access':
                    print('[==INFO==] check_access')
                    self.__granted['granted'] = 1 # это хард
                    message_reply.append(self.__granted)
                    continue
            except:
                print('[==INFO==] msg success')
                continue
        
        data = self.response_model(message_reply, self.data_request['sn'])
        print(f'[==INFO==] sent msg: -->> {data}')
        print(f'[==INFO==] end   -----------------------{timezone.now()}-----------------------')
        return JsonResponse(data)


    def response_model(self, message_reply: list | dict, serial_number_controller: int = None) -> dict:
        """
        Функция для типизации ответа.
        Args:
            message_reply (list | dict): принимает готовое
            сообщение или список таких сообщений, которые
            будут отправлены контроллеру.

        Returns:
            dict: объект Python для последущей трансформации
            в JSON.
        """
        date_time_created = timezone.now()
        date_time_created = date_time_created.strftime("%Y-%m-%d %H:%M:%S")

        self.__header_resonse['date'] = date_time_created
        self.__header_resonse['sn'] = serial_number_controller

        if isinstance(message_reply, list):
            self.__header_resonse["messages"] = message_reply
        else:
            self.__header_resonse["messages"] = [
                message_reply,
            ]
        return self.__header_resonse
    