import json, requests
from django.http import JsonResponse

from pprint import pprint

from django.utils import timezone
from django.db import models

from app_controller.models import Controller
from app_event.models import Event
from app_card_pass.models import CardPass


class BaseAdapterForModels:
    payload = None
    event_staff = 'Не известный'
    event_checkpoint = 'Не известная проходная'
    event_direction = 'Не известно направление'
    granted_0 = [2, 4, 6, 7, 14, 17, 26, 28, 30]
    event_serial_num_controller = None

    __controller: models = Controller
    __event: models = Event
    __card_pass: models = CardPass

    __header_resonse: dict = {"date": None, "interval": 10, "sn": None, "messages": None,}
    __set_mode: dict = {"id": 0, "operation": "set_mode", "mode": None}
    __set_active: dict = {"id": 0, "operation": "set_active", "active": None, "online": None}
    __granted = {"id": 0, "operation": "check_access", "granted": None}
    __resp_event = {"id":0, "operation": "events", "events_success": None}
  

    def __init__(self, request_adaptee, operition_type=None) -> None:
        self.request_adaptee = request_adaptee
        self.operition_type = operition_type


    def to_json(self) -> json:
        if b'operation' in self.request_adaptee.body:
            try:
                self.data_request = json.loads(self.request_adaptee.body)
                operition_type = self.data_request['messages'][0]['operation']
                return self.data_request, operition_type
            except json.decoder.JSONDecodeError:
                print(f'[== == ERROR == ==] Ошибка сериализации JSON!')
                return None
            except KeyError:
                print(f'[== == ERROR == ==] Ошибка доступа по ключу!')
                pprint(self.data_request, depth=4)
                return None
            except IndexError:
                print(f'[== == ERROR == ==] Ошибка доступа по индексу! Пустой список сообщений.')
                pprint(self.data_request, depth=4)
                return None
        return None


    def get_pass_number_to_dec_format(self, pass_number_hex):
        pass_number = int(pass_number_hex, base=16)
        count = 10 - len(str(pass_number))
        return f'{count*"0"}{pass_number}'


    def get_staff_init_event(self, pass_card_dec_format):
        try:
            staff_card = self.__card_pass.objects.get(pass_card_dec_format=pass_card_dec_format)
            self.event_staff = f'{staff_card.staff.last_name} {staff_card.staff.first_name} {staff_card.staff.patromic}'
            if staff_card.staff.interception or not staff_card.activate_card:
                self.__granted['granted'] = 0
        except self.__card_pass.DoesNotExist:
            self.__granted['granted'] = 0


    def get_place_init_event(self, serial_number):
        try:
            event_controller = self.__controller.objects.get(serial_number=serial_number)
            self.event_serial_num_controller = event_controller.get_serial_number_type_int
            self.event_checkpoint = event_controller.checkpoint
            self.event_direction = event_controller.direction
        except self.__controller.DoesNotExist:
            self.__granted['granted'] = 0
            self.event_serial_num_controller = serial_number


    def adapt_and_save(self) -> tuple[models.Model, dict, bool]:
            
            if self.operition_type == 'power_on':
                obj, create = self.__controller.objects.get_or_create(
                    type_controller = self.data_request['type'],
                    serial_number = self.data_request['sn']
                )
                if not create:
                    self.__set_active['active'] = int(obj.controller_activity)
                    self.__set_active['online'] = int(obj.controller_online.split('/')[0])
                    self.__set_mode['mode'] = int(obj.controller_online.split('/')[1])
                    message_reply = [self.__set_active, self.__set_mode]
                    self.payload = self.response_model(message_reply, obj.serial_number)
                    self.send_signal(obj.ip_adress, self.payload)
                    return self.response(self.payload, create)
                return self.response()                

            elif self.operition_type == 'events':
                list_events = self.data_request["messages"][0]["events"]

                for event in list_events:
                    self.__granted['granted'] = 1
                    event_date_time = event['time']

                    event_card_hex = event['card']
                    event_card_dec = self.get_pass_number_to_dec_format(event_card_hex)

                    event_type = event['event']
                    event_flag = event['flag']

                    self.get_staff_init_event(event_card_dec)
                    self.get_place_init_event(self.data_request['sn'])

                    if event_type in self.granted_0:
                        self.__granted['granted'] = 0

                    obj, create = self.__event.objects.get_or_create(
                        event_class = self.operition_type,
                        event_date_time = event_date_time,
                        event_card_hex = event_card_hex,
                        event_card_dec = event_card_dec,
                        event_staff = self.event_staff,
                        event_controller = self.event_serial_num_controller,
                        event_checkpoint = self.event_checkpoint,
                        event_direction = self.event_direction,
                        event_type = event_type,  
                        event_flag = event_flag,
                        event_granted = self.__granted['granted'],
                        event_package = event,
                    )

                self.__resp_event['events_success'] = len(list_events)
                data = self.response_model(self.__resp_event, self.event_serial_num_controller)
                return self.response(data, create)
            
            elif self.operition_type == 'check_access':
                self.__granted['granted'] = 1
                event_date_time = timezone.now()

                event_card_hex = self.data_request['messages'][0]['card']
                event_card_dec = self.get_pass_number_to_dec_format(event_card_hex)

                self.get_staff_init_event(event_card_dec)
                self.get_place_init_event(self.data_request['sn'])

                # if event_granted:
                    # self.__granted['granted'] = 1
                # activate_card = staff_card.activate_card,
                # еще проверки для 2 факторки и выдача разрешения

                obj, create = self.__event.objects.get_or_create(
                    event_class = self.operition_type,
                    event_date_time = event_date_time,
                    event_card_hex = event_card_hex,
                    event_card_dec = event_card_dec,
                    event_staff = self.event_staff,
                    event_controller = self.event_serial_num_controller,
                    event_checkpoint = self.event_checkpoint,
                    event_direction = self.event_direction,
                    event_type = '*',  event_flag = '*',
                    event_granted = self.__granted['granted'],
                    event_package = self.data_request,
                )

                data = self.response_model(self.__granted, self.event_serial_num_controller)
                return self.response(data=data, status_create=create)


    def response(self, data={}, status_create=None):
        resp = JsonResponse(data)
        if status_create: 
            resp.status_code = 201
        return resp


    def send_signal(self, url: str, payload: dict=None) -> int:
        try:
            resp = requests.post(url, data=payload)
        except Exception as e:
            print('[== ==ERROR== ==] Пакет не доставлен!')
            print(f'[== ==ERROR== ==] {e}')
            pprint(payload, depth=4)


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
