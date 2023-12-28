import json
from datetime import datetime

from django.http import JsonResponse

from django.utils import timezone
from django.db import models
from django.db.models import Q

from app_controller.models import Controller
from app_event.models import Event
from app_card_pass.models import CardPass

from django.core.cache import cache 


class BaseAdapterForModels:
    obj_staff = None
    event_staff = 'Не известный'
    event_checkpoint = 'Не известная проходная'
    event_direction = 'Не известно направление'
    granted_0 = [2, 3, 6, 7, 10, 11]
    event_table = {
        0: {'event': 'Открыто кнопкой изнутри', 'direction': 'ВХОД'},
        1: {'event': 'Открыто кнопкой изнутри', 'direction': 'ВЫХОД'},
        2: {'event': 'Ключ не найден в банке ключей', 'direction': 'ВХОД'},
        3: {'event': 'Ключ не найден в банке ключей', 'direction': 'ВЫХОД'},
        4: {'event': 'Ключ найден, дверь открыта', 'direction': 'ВХОД'},
        5: {'event': 'Ключ найден, дверь открыта', 'direction': 'ВЫХОД'},
        6: {'event': 'Ключ найден, доступ не разрешен', 'direction': 'ВХОД'},
        7: {'event': 'Ключ найден, доступ не разрешен', 'direction': 'ВЫХОД'},
        8: {'event': 'Открыто оператором по сети', 'direction': 'ВХОД'},
        9: {'event': 'Открыто оператором по сети', 'direction': 'ВЫХОД'},
        10: {'event': 'Ключ найден, дверь заблокирована', 'direction': 'ВХОД'},
        11: {'event': 'Ключ найден, дверь заблокирована', 'direction': 'ВЫХОД'},
    }

#  Нужно подумать о приватности и гетарах сетерах
    __controller: models = Controller
    __event: models = Event
    __card_pass: models = CardPass

    __header_resonse: dict = {"date": None, "interval": 10, "sn": None, "messages": None,}
    set_mode: dict = {"id": 0, "operation": "set_mode", "mode": None}
    set_active: dict = {"id": 0, "operation": "set_active", "active": None, "online": None}
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


    def adapt_and_save(self):
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
                        serial_number = self.data_request['sn'],
                        ip_adress = f"http://{messege['controller_ip']}"
                    )
                    if create:
                        continue
                    else:
                        self.set_active['active'] = int(obj.controller_activity)
                        self.set_active['online'] = int(obj.controller_online)
                        self.set_mode['mode'] = int(obj.controller_mode)
                        message_reply.extend([self.set_active, self.set_mode])
                        continue
                elif operations_type == 'events':
                    print('[==INFO==] events')
                    events = messege[operations_type]
                    self.__resp_event['events_success'] = len(events)
                    message_reply.append(self.__resp_event)
                    for event in events:
                        self.save_event(event, self.data_request['sn'])
                    continue
                elif operations_type == 'ping':
                    print('[==INFO==] ping')
                    if cache.get(self.data_request['sn']) != None:
                        message_reply.extend(cache.get(self.data_request['sn']))
                    if cache.get(f'{self.data_request["sn"]}_add_cards') != None:
                        add_cards = cache.get(f'{self.data_request["sn"]}_add_cards')
                        print(f"add_cards --- {add_cards}")
                        message_reply.extend(add_cards)
                    if cache.get(f'{self.data_request["sn"]}_del_cards') != None:
                        del_cards = cache.get(f'{self.data_request["sn"]}_del_cards')
                        print(f"del_cards --- {del_cards}")
                        message_reply.extend(del_cards)
                    cache.delete(self.data_request['sn'])
                    cache.delete(f'{self.data_request["sn"]}_add_cards')
                    cache.delete(f'{self.data_request["sn"]}_del_cards')
                    continue
                elif operations_type == 'check_access':
                    print('[==INFO==] check_access')
                    self.__granted['granted'] = 1 # это хард!!!!!!!!!!!!!!!!!!!!
                    message_reply.append(self.__granted)
                    continue
            except KeyError:
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
    

    def save_event(self, event, sn_controller):
        number_event = event['event']
        event_time = datetime.strptime(event['time'], "%Y-%m-%d %H:%M:%S")

        if number_event not in self.event_table:
            return

        event_card_dec = self.get_pass_number_to_dec_format(event['card'])
        self.get_staff_init_event(event_card_dec)
        self.get_place_init_event(sn_controller, event)
        self.get_late_status(event_time)
        
        obj, create = self.__event.objects.get_or_create(
            event_date_time = event['time'],
            event_card_hex = event['card'],
            event_card_dec = event_card_dec,
            event_staff = self.event_staff,
            event_controller = sn_controller,
            event_checkpoint = self.event_checkpoint,
            event_direction = self.event_direction,
            event_type = self.event_table[event['event']]['event'],  
            event_flag = event['flag'],
            event_granted = self.get_granted_to_event(event),
            event_package = event,
            late = self.__late,
            event_late_status = self.__late_status,
            ENTRY_EXIT_queue_broken = self.__queue_broken,
        )


    def get_pass_number_to_dec_format(self, pass_number_hex):
        # 004E0019C52A используются не короткие ключи, поэтому беру срез
        pass_number = int(pass_number_hex[6:], base=16)
        count = 10 - len(str(pass_number))
        return f'{count*"0"}{pass_number}'
    

    def get_granted_to_event(self, event):
        if event['event'] in self.granted_0:
            return False
        return True
    

    def get_reason_granted_to_event(self, event):
        pass
    

    def get_staff_init_event(self, pass_card_dec_format):
        try:
            staff_card = self.__card_pass.objects.get(pass_card_dec_format=pass_card_dec_format)
            self.obj_staff = staff_card.staff
            self.event_staff = f'{staff_card.staff.last_name} {staff_card.staff.first_name} {staff_card.staff.patromic}'
            if staff_card.staff.interception or not staff_card.activate_card:
                self.__granted['granted'] = 0
        except self.__card_pass.DoesNotExist:
            self.__granted['granted'] = 0

    
    def get_place_init_event(self, serial_number, event):
        try:
            event_controller = self.__controller.objects.get(serial_number=serial_number)
            event_checkpoint = event_controller.checkpoint
            if event_checkpoint != None:
                self.event_checkpoint = event_checkpoint
            if event_controller.direction == '0':
                self.event_direction = self.event_table[event['event']]['direction']
            else:
                self.event_direction = event_controller.direction
        except self.__controller.DoesNotExist:
            self.__granted['granted'] = 0


    def get_late_status(self, event_date_time):
        event_time = event_date_time.time()
        event_date = event_date_time.date()
        week_day = self.week_days[event_date.weekday()]
        if self.obj_staff == None:
            return
        for day_schedule in self.obj_staff.schedule.day_set.all():
            if week_day == day_schedule.week_day:
                self.schedule_for_today = day_schedule
        events_staff_today = self.__event.objects.filter(
                    Q(event_staff=self.event_staff), Q(event_date_time__date=event_date))
        if events_staff_today.last() is None and self.schedule_for_today is not None:
            if self.event_direction == 'ВХОД':
                if self.schedule_for_today.day_time_start < event_time:
                    self.__late = True
                    self.__late_status = f'''Опоздание на {
                        event_date_time - datetime.combine(event_date, self.schedule_for_today.day_time_start)
                    }'''
            else:
                self.__queue_broken = True
                self.__late_status = 'Не известно время выхода'
        elif events_staff_today.last() is not None and self.schedule_for_today is not None:
            time_interval_before_break = [self.schedule_for_today.day_time_start, self.schedule_for_today.break_in_schedule_start]
            time_interval_after_break = [self.schedule_for_today.break_in_schedule_end, self.schedule_for_today.day_time_end]
            if self.schedule_for_today.break_in_schedule_start is None or \
                self.schedule_for_today.break_in_schedule_end is None:
                time_interval_before_break[1] = self.schedule_for_today.day_time_end
                time_interval_after_break[0] = self.schedule_for_today.day_time_start
            if self.event_direction == 'ВЫХОД':
                if time_interval_before_break[0] < event_time < time_interval_before_break[1]:
                    self.__late_status = f'''До конца рабочего дня осталось: {
                        datetime.combine(event_date, time_interval_before_break[1]) - event_date_time
                    }'''
                if time_interval_after_break[0] < event_time < time_interval_after_break[1]:
                    self.__late_status = f'''До конца рабочего дня осталось: {
                        datetime.combine(event_date, time_interval_after_break[1]) - event_date_time
                    }'''
            else:
                if time_interval_after_break[0] < event_time < time_interval_after_break[1]:
                    e = self.__event.objects.filter(
                    Q(event_date_time__range=(
                            str(datetime.combine(event_date, time_interval_after_break[0])),
                            str(datetime.combine(event_date, time_interval_after_break[1])))
                    ))
                    if e.count() == 0:
                        self.__late_status = f'''Опоздание на {
                            event_date_time - datetime.combine(event_date, time_interval_after_break[0])}'''
        if events_staff_today.last() is not None and events_staff_today.last().event_direction == self.event_direction:
                self.__queue_broken = True
