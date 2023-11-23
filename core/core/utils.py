import json, requests

from pprint import pprint

from datetime import datetime

from django.db import models

from app_controller.models import Controller


class BaseAdapterForModels:
    payload = None

    __controller: models = Controller

    __header_resonse: dict = {"date": None, "interval": 10, "sn": None, "messages": None,}

    __set_mode: dict = {"id": 0, "operation": "set_mode", "mode": None}

    __set_active: dict = {"id": 0, "operation": "set_active", "active": None, "online": None}

  

    def __init__(self, model, request_adaptee) -> None:
        self.model = model
        self.controller_adaptee = request_adaptee


    def to_json(self) -> json:
        try:
            self.data_request = json.loads(self.controller_adaptee.body)
            return self.data_request
        except json.decoder.JSONDecodeError:
            raise ValueError('Не могу преобразовать полученные данные в формат JSON.')

    
    def get_message_from_controller(self):
        try:
            return self.to_json()['messages']
        except KeyError:
            raise KeyError('Не согу извлеть ключ <messages>')
        

    def select_message(self, operation_type=None):
        messages = self.get_message_from_controller()
        if operation_type == None:
            return messages
        for i in messages:
            if operation_type == i['operation']:
                return i
        

    def get_list_type_masseges(self):
        list_type_message = []
        for msg in self.get_message_from_controller():
            try:
                list_type_message.append(msg['operation'])
            except KeyError:
                print(f'[== == ERROR == ==] Нет ключа <operation> в сообщении от контроллера!')
        return list_type_message


    def adapt_and_save(self) -> tuple[models.Model, dict, bool]:
        for operation in self.get_list_type_masseges():
            if operation == 'power_on' and issubclass(self.model, self.__controller):
                obj, create = self.model.objects.get_or_create(
                    type_controller = self.data_request['type'],
                    serial_number = self.data_request['sn']
                )

                if not create:
                    self.__set_active['active'] = int(obj.controller_activity)
                    self.__set_active['online'] = int(obj.controller_online.split('/')[0])
                    self.__set_mode['mode'] = int(obj.controller_online.split('/')[1])
                    message_reply = [self.__set_active, self.__set_mode]
                    payload = self.response_model(message_reply, obj.serial_number)
                
                return obj, payload, create

            elif operation == 'ANY':
                pass
            elif operation == 'ANYANY':
                pass

            
    def send_signal(self, url: str, payload: dict=None) -> int:
        try:
            resp = requests.post(url, data=payload)
            return 200
        except Exception as e:
            print('[== ==ERROR== ==] Пакет не доставлен!')
            pprint(payload, depth=4)
            return 400

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
        date_time_created = datetime.now()
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
