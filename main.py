from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.properties import (
    ObjectProperty, StringProperty, DictProperty, BooleanProperty, NumericProperty)
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.filechooser import FileChooserIconView
from methods import *
import math
import os


class Container(BoxLayout):

    def start(self):
        self.ds.text = ''
        self.hash_output.text = ''
        self.input_text.text = ''
        filename = self.input_file_name.text
        try:
            with open(filename, 'rb') as f:
                input_text = f.read()
            if self.type_of_code.text == 'Постановка ЭЦП':
                self.make_digital_signature(input_text)
            else:
                self.make_checking(input_text)
        except FileNotFoundError:
            self.lbl_error_file.color = (1, 0, 0, 1)

    def make_digital_signature(self, input_text):
        filename = self.input_file_name.text
        try:
            if not self.key_q.text.isdigit() or not self.check_prime(int(self.key_q.text)):
                raise ValueError_q
            if not self.key_p.text.isdigit() or not self.check_prime(int(self.key_p.text)):
                raise ValueError_p
            if (int(self.key_p.text) - 1) % int(self.key_q.text) != 0 or int(self.key_p.text) < int(self.key_q.text):
                raise ValueError_p
            if not self.key_h.text.isdigit() or not (1 < int(self.key_h.text) < int(self.key_p.text) - 1):
                raise ValueError_h
            if not self.key_x.text.isdigit() or not (0 < int(self.key_x.text) < int(self.key_q.text)):
                raise ValueError_x
            if not self.key_k.text.isdigit() or not (0 < int(self.key_k.text) < int(self.key_q.text)):
                raise ValueError_k
            hash, r, s = DSA(filename, int(self.key_q.text), int(self.key_p.text), int(
                self.key_h.text), int(self.key_x.text), int(self.key_k.text))
            self.hash_output.text = str(hash) + '\n' + hex(hash)
            self.ds.text = 'r = {}\ns = {}'.format(r, s)
        except ValueError_p:
            self.lbl_error_key_p.color = (1, 0, 0, 1)
            self.lbl_error_key_p.text = 'p не простое'
            if (int(self.key_p.text) - 1) % int(self.key_q.text) != 0 or int(self.key_p.text) < int(self.key_q.text):
                self.lbl_error_key_p.text = 'q не делитель p - 1'
        except ValueError_q:
            self.lbl_error_key_q.color = (1, 0, 0, 1)
            self.lbl_error_key_q.text = 'q не простое'
        except ValueError_x:
            self.lbl_error_key_x.color = (1, 0, 0, 1)
            self.lbl_error_key_x.text = 'x не соответсвует начальным условиям'
        except ValueError_h:
            self.lbl_error_key_h.color = (1, 0, 0, 1)
            self.lbl_error_key_h.text = 'h не соответсвует начальным условиям'
        except ValueError_k:
            self.lbl_error_key_k.color = (1, 0, 0, 1)
            self.lbl_error_key_k.text = 'k не соответсвует начальным условиям'
        except ValueError:
            self.lbl_error_key_k.color = (1, 0, 0, 1)
            self.lbl_error_key_k.text = 'Один из компонентов ЭЦП равен 0. Выберите другое k'

    def make_checking(self, input_text):
        filename = self.input_file_name.text
        try:
            if not self.key_q.text.isdigit() or not self.check_prime(int(self.key_q.text)):
                raise ValueError_q
            if not self.key_p.text.isdigit() or not self.check_prime(int(self.key_p.text)):
                raise ValueError_p
            if (int(self.key_p.text) - 1) % int(self.key_q.text) != 0 or int(self.key_p.text) < int(self.key_q.text):
                raise ValueError_p
            if not self.key_h.text.isdigit() or not (1 < int(self.key_h.text) < int(self.key_p.text) - 1):
                raise ValueError_h
            if not self.key_x.text.isdigit() or not (0 < int(self.key_x.text) < int(self.key_q.text)):
                raise ValueError_x
            if not self.key_k.text.isdigit() or not (0 < int(self.key_k.text) < int(self.key_q.text)):
                raise ValueError_k
            is_correct, v, r = check_digital_signature(filename, int(self.key_q.text), int(
                self.key_p.text), int(self.key_h.text), int(self.key_x.text), int(self.key_k.text))
            if is_correct:
                self.input_text.text = 'ЭЦП подлинно \nv = r = {}'.format(v)
            else:
                if r:
                    self.input_text.text = 'ЭЦП не подлинно \nv = {} \nr = {}'.format(
                        v, r)
                else:
                    self.input_text.text = 'ЭЦП не подлинно \nОшибка чтения подписи'
        except ValueError_p:
            self.lbl_error_key_p.color = (1, 0, 0, 1)
            self.lbl_error_key_p.text = 'p не простое'
            if (int(self.key_p.text) - 1) % int(self.key_q.text) != 0 or int(self.key_p.text) < int(self.key_q.text):
                self.lbl_error_key_p.text = 'q не делитель p - 1'
        except ValueError_q:
            self.lbl_error_key_q.color = (1, 0, 0, 1)
            self.lbl_error_key_q.text = 'q не простое'
        except ValueError_x:
            self.lbl_error_key_x.color = (1, 0, 0, 1)
            self.lbl_error_key_x.text = 'x не соответсвует начальным условиям'
        except ValueError_h:
            self.lbl_error_key_h.color = (1, 0, 0, 1)
            self.lbl_error_key_h.text = 'h не соответсвует начальным условиям'
        except ValueError_k:
            self.lbl_error_key_k.color = (1, 0, 0, 1)
            self.lbl_error_key_k.text = 'k не соответсвует начальным условиям'
        except ValueError:
            self.lbl_error_key_k.color = (1, 0, 0, 1)
            self.lbl_error_key_k.text = 'Один из компонентов ЭЦП равен 0. Выберите другое k'

    @staticmethod
    def check_prime(number):
        root = int(math.sqrt(number))
        if number < 2:
            return False
        for divider in range(2, root):
            if number % divider == 0:
                return False
        return True


class InputKey(TextInput):
    pass


class MethodSpinner(Spinner):

    active_method = StringProperty('Постановка ЭЦП')

    def clean_input(self):
        root = App.get_running_app().root.get_screen('main').container
        if self.active_method != self.text:
            self.active_method = self.text
            root.ds.text = ''
            root.hash_output.text = ''
            root.input_text.text = ''
            root.input_file_name.text = ''


class MainScreen(Screen):
    pass


class FileChooserScreen(Screen):
    pass


class BtnOpenFile(Button):

    def get_path(self):
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests/')


class ChoosingFile(FileChooserIconView):

    def fill_text(self):
        self._update_files()
        root = App.get_running_app().root
        root.current = 'main'
        if self.selection != []:
            root.get_screen('main').container.input_file_name.text = (
                self.selection[0].replace('tests/', '', 1))


class MyApp(App):

    def build(self):
        sm = ScreenManager()
        self.sm = sm
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(FileChooserScreen(name='filechooser'))
        return self.sm


class ValueError_p(Exception):
    pass


class ValueError_q(Exception):
    pass


class ValueError_x(Exception):
    pass


class ValueError_k(Exception):
    pass


class ValueError_h(Exception):
    pass


if __name__ == '__main__':
    MyApp().run()
