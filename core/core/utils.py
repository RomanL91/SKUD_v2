import json

from app_controller.models import Controller


class BaseAdapterForModels:
    __controller = Controller

    def __init__(self, model, request_adaptee) -> None:
        self.model = model
        self.controller_adaptee = request_adaptee


    def to_json(self):
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


    def adapt_and_save(self):
        for operation in self.get_list_type_masseges():
            if operation == 'power_on' and issubclass(self.model, self.__controller):
                obj, create = self.model.objects.get_or_create(
                    type_controller = self.data_request['type'],
                    serial_number = self.data_request['sn']
                )
                return obj, create
            

    async def send_signal(self):
        pass


    


    