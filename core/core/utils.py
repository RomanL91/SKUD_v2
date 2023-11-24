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



    __controller: models = Controller
    __event: models = Event
    __card_pass: models = CardPass

    __header_resonse: dict = {"date": None, "interval": 10, "sn": None, "messages": None,}
    __set_mode: dict = {"id": 0, "operation": "set_mode", "mode": None}
    __set_active: dict = {"id": 0, "operation": "set_active", "active": None, "online": None}
    __granted = {"id": 0, "operation": "check_access", "granted": 1}
  

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


    # Переписать, возможно разнести, может использовать конструкцию switch case
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
                    resp = JsonResponse(self.payload)
                    resp.status_code = 200
                    return resp
                
                resp = JsonResponse({})
                resp.status_code = 201
                return resp 

            elif self.operition_type == 'events' and issubclass(self.model, self.__event):
                print('----->>> ENENT 1 factor')
                return (1, 2, 3)
            elif self.operition_type == 'check_access':
                event_date_time = timezone.now()

                event_card_hex = self.data_request['messages'][0]['card']
                event_card_dec = int(event_card_hex, base=16)
                count = 10 - len(str(event_card_dec))
                event_card_dec = f'{count*"0"}{event_card_dec}'
                try:
                    staff_card = self.__card_pass.objects.get(pass_card_dec_format=event_card_dec)
                    self.event_staff = staff_card.staff
                except self.__card_pass.DoesNotExist:
                    print('tyt')
                    self.__granted['granted'] = 0
                try:
                    event_controller = self.__controller.objects.get(serial_number=self.data_request['sn'])
                    event_serial_num_controller = event_controller.get_serial_number_type_int
                    self.event_checkpoint = event_controller.checkpoint
                    self.event_direction = event_controller.direction
                except self.__controller.DoesNotExist:
                    print('tyt2')
                    self.__granted['granted'] = 0
                    event_serial_num_controller = self.data_request["sn"]

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
                    event_controller = event_serial_num_controller,
                    event_checkpoint = self.event_checkpoint,
                    event_direction = self.event_direction,
                    event_type = '*',  event_flag = '*',
                    event_granted = self.__granted['granted'],
                    event_package = self.data_request,
                )

                data = self.response_model(self.__granted, event_serial_num_controller)
                resp = JsonResponse(data)
                resp.status_code = 201
                return resp
            
    def send_signal(self, url: str, payload: dict=None) -> int:
        try:
            resp = requests.post(url, data=payload)
        except Exception as e:
            print('[== ==ERROR== ==] Пакет не доставлен!')
            print(f'[== ==ERROR== ==] {e}')
            pprint(payload, depth=4)

    # async def send_signal(self):
    #     payload = {'key1': 'value1', 'key2': 'value2'}
    #     async with aiohttp.ClientSession() as session:
    #         async with session.post('http://httpbin.org/post', data=payload) as resp:
    #              print(await resp.text())


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
