from re import match, findall
from random import randint
from logics import CS_Remember_Logic
from kivy.utils import get_color_from_hex
from kivy.uix.pagelayout import PageLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import RoundedRectangle

from kivy.graphics import RoundedRectangle, Color
# Потключение виртуальной клавиотуры
Config.set("kivy", "keyboard_mode", "systemanddock")


# Операционная система
# pc | phone
PLATFORM = 'pc'


class Container (PageLayout):

    Color_Background = get_color_from_hex("#1E4457")
    Color_Contant = get_color_from_hex("#98AEBB")

    Color_Duble = get_color_from_hex("#000000")
    Color_Text_Inpyt = get_color_from_hex("#000000")
    Color_Button = Color_Contant
    Color_Background_Text_Inpyt = Color_Button

    Color_True = get_color_from_hex("#66D400")
    Color_False = get_color_from_hex("#D35E54")
    Color_Yellow = get_color_from_hex("#D3BD54")

    # Логика
    DCS_logics = CS_Remember_Logic()
    ############################################################
    # Страница с вопросами
    pagemain = ObjectProperty()
    # Контейнер с <textinput_main> <button_send> <label_flag> <label_main>
    boxLayout_keyboard = ObjectProperty()
    # Имя флага который показан
    label_flag = ObjectProperty()
    # Текстовое поле с вопросом
    label_main = ObjectProperty()
    # Текстовое поля для ввода ответа
    textinput_main = ObjectProperty()
    # Кнопка - отправить резултат с клавиатуры
    button_send = ObjectProperty()
    # Контейнер с кнопкапи ответов
    gridlayout_options_response = ObjectProperty()
    # Кнопки в выбором ответа
    butt_send10 = ObjectProperty()
    butt_send20 = ObjectProperty()
    butt_send30 = ObjectProperty()
    butt_send40 = ObjectProperty()
    optionsbutton_list = []
    # Для переключения флагов
    trigger = 0
    #-----------------------------------------------------------#
    # Страница с настройками
    pagesatting = ObjectProperty()
    # Список флагов
    listFlag = ObjectProperty()
    # Флаги выбранные пользователем
    selected_user_flag = []
    # Массив со всеми флагами
    list_flag_json = []
    # Кнопка перелистования на главную страницу
    button_sewap_pagemain = ObjectProperty()
    # Текстовое поля ввода индексов флага
    text_input_flag = ObjectProperty()
    ############################################################

    text_input_boxlayout = ObjectProperty()
    boxlayout_options_buuton = ObjectProperty()
    setttings = ObjectProperty()

    text_question_boxlayout = ObjectProperty()
    text_statistic_boxlayout = ObjectProperty()

    save_flag = ObjectProperty()

    switch_iput = ObjectProperty()
    switch_revers = ObjectProperty()

    bolvanca_flag = ObjectProperty()
    bolvanca_main = ObjectProperty()

    out_flag_0 = ObjectProperty()
    out_flag_1 = ObjectProperty()
    out_flag_2 = ObjectProperty()

    left_swap_node = ObjectProperty()
    len_flag_label = ObjectProperty()
    right_swap_node = ObjectProperty()

    сell_node = ObjectProperty()

    # Для перемещения по флагам
    lenger_swap_flag = 0
    ############################################################
    # Обнавление кнопок с ответами

    def Refresh_Options(self):

        if self.DCS_logics.index_all_array_sentences:
            a = []
            m = max(self.DCS_logics.index_all_array_sentences)
            if m >= 3:
                for x in range(3):
                    a.append(randint(x, m))
                a.insert(randint(0, 3),
                         self.DCS_logics.index_all_array_sentences[0])

            else:
                a = [self.DCS_logics.index_all_array_sentences[0],
                     self.DCS_logics.index_all_array_sentences[0],
                     self.DCS_logics.index_all_array_sentences[0],
                     self.DCS_logics.index_all_array_sentences[0]]

            self.optionsbutton_list = [
                self.butt_send10, self.butt_send20, self.butt_send30, self.butt_send40]
            self.optionsbutton_list[0].text = self.DCS_logics.list_all_text[a[0]]["2"]
            self.optionsbutton_list[1].text = self.DCS_logics.list_all_text[a[1]]["2"]
            self.optionsbutton_list[2].text = self.DCS_logics.list_all_text[a[2]]["2"]
            self.optionsbutton_list[3].text = self.DCS_logics.list_all_text[a[3]]["2"]

    # Проверка отывета пользователя с кнопок

    def Verify_User_Options(self, text, ids):
        def New_sentence():

            self.trigger = 0

            for x in self.optionsbutton_list:
                x.canvas.before.children[0].rgba = self.Color_Button

            if self.DCS_logics.index_all_array_sentences:
                self.label_main.text = self.DCS_logics.list_all_text[
                    self.DCS_logics.index_all_array_sentences[0]]["1"]
                self.label_flag.text = "{}: {}".format(
                    self.DCS_logics.list_all_text[self.DCS_logics.index_all_array_sentences[0]]["0"], self.DCS_logics.list_all_text[self.DCS_logics.index_all_array_sentences[0]]["4"])
                self.Refresh_Options()

            else:
                self.DCS_logics.Save_Result()
                self.DCS_logics.Creating_Array_Sentences()
                ###
                self.Refresh_Options()
                New_sentence()

        if not self.trigger:

            # Если есть предложения показываем их, и удаляем первое
            if self.DCS_logics.index_all_array_sentences:
                a = text.lower().strip()
                b = self.DCS_logics.list_all_text[self.DCS_logics.index_all_array_sentences[0]]
                # Правильный овтет
                if a == b["2"].lower().strip():
                    if int(b["4"]) < 6:
                        b["4"] = str(int(b["4"]) + 1)
                    # GREAN
                    ids.canvas.before.children[0].rgba = self.Color_True

                # Неправильынй ответ
                else:
                    # Штраф в 3 еденицы
                    if int(b["4"]) >= 3:
                        b["4"] = str(int(b["4"]) - 3)
                        # ELow
                        ids.canvas.before.children[0].rgba = self.Color_Yellow

                    else:
                        b["4"] = str(int(b["4"]) - 1)
                        # READ
                        ids.canvas.before.children[0].rgba = self.Color_False

                    # Показать кнопку с верныйм ответом

                    for x in self.optionsbutton_list:
                        if x.text == b["2"]:
                            x.canvas.before.children[0].rgba = self.Color_True

                self.DCS_logics.index_all_array_sentences.pop(0)
                self.trigger = 1

            else:
                New_sentence()

        else:
            New_sentence()

    # Функция переключения способа ответа
    def Switch_Response_Method(self, switchValue):
        # a = self.pagesatting.children[0]
        # On 4 варианта ответ
        if switchValue.state == "down":
            self.Show_Options_Response()
        # Off ввод с клавиотуры
        else:
            self.Show_Keyboard_Response()

    # Показать вариант с клавиотурой
    def Show_Keyboard_Response(self):
        # Показать поле ввода и кнопку
        self.boxLayout_keyboard.size_hint_y = 0.1
        self.boxLayout_keyboard.opacity = 1
        # Скрыть кнопки овтетов, они должны уменьшаться чтобы невылазить
        self.gridlayout_options_response.opacity = 0
        self.gridlayout_options_response.size_hint_y = None
        self.gridlayout_options_response.height = '0'
        self.Next_Word()

    # Показать вариант с кнопками
    def Show_Options_Response(self):
        # Скрыть поле ввода и кнопку
        self.boxLayout_keyboard.size_hint_y = 0.1
        self.boxLayout_keyboard.opacity = 0
        # Отчистка поля ввода
        self.textinput_main.text = ""
        # Показать кнопки ответов, они должны уменьшаться чтобы невылазить
        self.gridlayout_options_response.size_hint_y = 0.6
        self.gridlayout_options_response.opacity = 1
        self.Refresh_Options()

    def Switch_Order(self, switchValue):

        for i in range(len(self.DCS_logics.list_all_text)):
            self.DCS_logics.list_all_text[i]['1'], self.DCS_logics.list_all_text[i][
                '2'] = self.DCS_logics.list_all_text[i]['2'], self.DCS_logics.list_all_text[i]['1']

        self.DCS_logics.Save_Result()

    ############################################################
    # Поднятие клавиатуры в настройках
    def Text_Input_Flag_on_focus(self, value):
        if PLATFORM == "phone":
            if value:
                self.bolvanca_flag.size_hint_y = 0.5
                self.setttings.size_hint_y = 0.1
                self.text_input_boxlayout.size_hint_y = 0.1
                self.boxlayout_options_buuton.size_hint_y = 0.3

            else:
                self.bolvanca_flag.size_hint_y = None
                self.bolvanca_flag.height = '0'
                self.setttings.size_hint_y = 0.1
                self.text_input_boxlayout.size_hint_y = 0.1
                self.boxlayout_options_buuton.size_hint_y = 0.8

            # Полнятие клавиатуры в на главной старанице

    def Text_Input_Response_on_focus(self, value):
        if PLATFORM == "phone":
            if value:
                self.bolvanca_main.size_hint_y = 0.5
                self.text_statistic_boxlayout.size_hint_y = 0.07
                self.text_question_boxlayout.size_hint_y = 0.3
                self.boxLayout_keyboard.size_hint_y = 0.1

            else:
                self.bolvanca_main.size_hint_y = None
                self.bolvanca_main.height = '0'
                self.text_statistic_boxlayout.size_hint_y = 0.07
                self.text_question_boxlayout.size_hint_y = 0.8
                self.boxLayout_keyboard.size_hint_y = 0.1

        if not value and self.textinput_main.text != '':
            self.Verify_User_Response()
    ############################################################

    ############################################################
    # Переключиться в Настройки из главной страницы

    def SwapSettings(self):
        # Сохраняем результат ответов
        self.DCS_logics.Save_Result()
        # Переключаемся на в найтроки
        self.page = 1

    # Переключиться на главную страницу из настроики
    def SewapPagemain(self):
        # Если флаги не выбраны то не переходим на главную страницу
        if not self.selected_user_flag:
            self.button_sewap_pagemain.background_down = './ico/Qarrow_L.png'
            self.button_sewap_pagemain.canvas.before.children[0].rgba = self.Color_False
            # self.button_sewap_pagemain.text = "X"
            # self.button_sewap_pagemain.background_color = get_color_from_hex("#D35E54")
            return False

        # Конвертируем значения из таблицы
        self.DCS_logics.selected_flags_user = self.selected_user_flag

        # Создаем список предложений
        self.DCS_logics.Creating_Array_Sentences()
        # Показываем предложение
        self.Next_Word()

        #!!! На сулачай если перейти из главного окна в настройки при вариативном ответе
        self.Refresh_Options()

        # Скидываем цвет кнопку в исходынй
        self.button_sewap_pagemain.background_down = './ico/Qarrow_R.png'
        self.button_sewap_pagemain.canvas.before.children[0].rgba = self.Color_Button
        # Переключаемся на главный слой
        self.page = 0

        return True

    # Переключаемся на страницу добавление предложений из настроики
    def SewapWriteFlags(self):
        #
        self.page = 2

    # Переключаемся на в настроики из добавления предложений
    def Settings_SewapWriteFlags(self):
        #
        self.page = 1
    ############################################################

    ############################################################
    # Добовляем флаг

    def Add_Flag(self):

        if self.out_flag_0.text and self.out_flag_1.text and self.out_flag_2.text:
            outputtextflag = '0:{}\n1:{}\n2:{}\n'.format(self.out_flag_0.text,
                                                         self.out_flag_1.text,
                                                         self.out_flag_2.text)
            if self.DCS_logics.Add_Flag(outputtextflag):
                self.DCS_logics.Restart_Data()
                #self.out_flag_0.text = ''
                self.out_flag_1.text = ''
                self.out_flag_2.text = ''
                self.save_flag.canvas.before.children[0].rgba = self.Color_True
                return True
            else:
                self.save_flag.canvas.before.children[0].rgba = self.Color_False
                return False

        else:
            self.save_flag.canvas.before.children[0].rgba = self.Color_Button
            return None

    ############################################################
    # Функция для записи флагов. <bind ToggleButton>

    def Selekt_Flag(self, box_l, but_t):

        # Записываем нажатые флаги в массив, для дальнейше обработки
        self.selected_user_flag = list(set(self.selected_user_flag))
        a = findall(r'\d+\)+([^[]+)', but_t.text)[0].strip()
        if but_t.state == 'down':
            if a in [x[0]for x in self.DCS_logics.flags]:
                self.selected_user_flag.append(a)
                return True

        self.selected_user_flag.remove(a)
        return False

    # Обновить списко флагов
    def Manager_Flags(self) -> bool:
        # Получам флаги из базы
        self.DCS_logics.Restart_Data()
        self.list_flag_json = self.DCS_logics.Respose_Flag()
        # Обновляем список флагов
        self.boxlayout_options_buuton.clear_widgets()
        self.boxlayout_options_buuton.canvas.before.children[0].rgba = self.Color_Background
        # Обновление цвета у кнопок
        self.right_swap_node.canvas.before.children[0].rgba = self.Color_Button
        self.left_swap_node.canvas.before.children[0].rgba = self.Color_Button
        # Максималья длинна флага
        self.len_flag_label.text = str(len(self.list_flag_json))
        self.lenger_swap_flag = 0
        # Создаем таблицу
        for x in self.list_flag_json[5*self.lenger_swap_flag:(5*self.lenger_swap_flag)+5:]:
            self.w = Builder.load_string("""
BoxLayout:
    ToggleButton:
        background_color: Color_Contant
        text:"..."
        font_size: '25sp'
        color: Color_Text_Inpyt
        background_normal:''
        background_down:'./ico/green.png'
        on_state:app.layout.Selekt_Flag(app.layout,self)
            """)

            self.w.children[0].text = r"{})  {}   [{} : {} : {}]".format(
                x[0], x[1], x[2], x[3], x[4])

            if self.DCS_logics.flags[int(
                    findall(r'(\d+)[)]', self.w.children[0].text)[0])-1][0] in self.selected_user_flag:
                self.w.children[0].state = 'down'

            self.boxlayout_options_buuton.add_widget(self.w)
    #
    # Перелистунть список флагов влево

    def Swap_Left_List_Flag(self):
        # Ограничители передвижения
        if self.lenger_swap_flag-1 < 0:
            self.left_swap_node.canvas.before.children[0].rgba = self.Color_False
            return False
        # Обновление цвета у кнопок
        self.right_swap_node.canvas.before.children[0].rgba = self.Color_Button
        self.left_swap_node.canvas.before.children[0].rgba = self.Color_Button
        # готовим даннеы для записи
        self.boxlayout_options_buuton.clear_widgets()
        self.boxlayout_options_buuton.canvas.before.children[0].rgba = self.Color_Background
        self.lenger_swap_flag -= 1
        # Состовляем таблицу
        for x in self.list_flag_json[5*self.lenger_swap_flag:(5*self.lenger_swap_flag)+5:]:
            self.w = Builder.load_string("""
BoxLayout:
    ToggleButton:
        background_color: Color_Contant
        text:"..."
        font_size: '20sp'
        background_normal:''
        background_down:'./ico/green.png'
        on_state:app.layout.Selekt_Flag(app.layout,self)
                """)
            self.w.children[0].text = r"{})  {}   [{} : {} : {}]".format(
                x[0], x[1], x[2], x[3], x[4])

            if self.DCS_logics.flags[int(
                    findall(r'(\d+)[)]', self.w.children[0].text)[0])-1][0] in self.selected_user_flag:
                self.w.children[0].state = 'down'

            self.boxlayout_options_buuton.add_widget(self.w)
    #
    # Перелистунть список флагов вправо

    def Swap_Right_List_Flag(self):
        # Ограничители передвижения
        if self.lenger_swap_flag+1 > (int(self.len_flag_label.text)-1)//5:
            self.right_swap_node.canvas.before.children[0].rgba = self.Color_False
            return False
        # Обновление цвета у кнопок
        self.right_swap_node.canvas.before.children[0].rgba = self.Color_Button
        self.left_swap_node.canvas.before.children[0].rgba = self.Color_Button
        # готовим даннеы для записи
        self.boxlayout_options_buuton.clear_widgets()
        self.boxlayout_options_buuton.canvas.before.children[0].rgba = self.Color_Background
        self.lenger_swap_flag += 1
        # Состовляем таблицу
        for x in self.list_flag_json[5*self.lenger_swap_flag:(5*self.lenger_swap_flag)+5:]:
            self.w = Builder.load_string("""
BoxLayout:
    ToggleButton:
        background_color: Color_Contant
        text:"..."
        font_size: '20sp'
        background_normal:''
        background_down:'./ico/green.png'
        on_state:app.layout.Selekt_Flag(app.layout,self)
                """)
            self.w.children[0].text = "{})  {}   [{} : {} : {}]".format(
                x[0], x[1], x[2], x[3], x[4])

            if self.DCS_logics.flags[int(
                    findall(r'(\d+)[)]', self.w.children[0].text)[0])-1][0] in self.selected_user_flag:
                self.w.children[0].state = 'down'

            self.boxlayout_options_buuton.add_widget(self.w)
        return True

    ############################################################

    ############################################################
    # Показать новео слово

    def Next_Word(self, recus=False):

        self.button_send.text = '^'
        self.textinput_main.text = ''
        self.trigger = 0
        self.button_send.canvas.before.children[0].rgba = self.Color_Button

        if self.DCS_logics.index_all_array_sentences:
            self.label_main.text = self.DCS_logics.list_all_text[
                self.DCS_logics.index_all_array_sentences[0]]["1"]
            self.label_flag.text = "{}: {}".format(
                self.DCS_logics.list_all_text[self.DCS_logics.index_all_array_sentences[0]]["0"], self.DCS_logics.list_all_text[self.DCS_logics.index_all_array_sentences[0]]["4"])

        else:
            self.DCS_logics.Save_Result()
            self.DCS_logics.Creating_Array_Sentences()
            if not recus:
                self.Next_Word(True)

    # Проверка ответа пользователя
    def Verify_User_Response(self):

        if not self.trigger:

            # Если есть предложения показываем их, и удаляем первое
            if self.DCS_logics.index_all_array_sentences:
                a = self.textinput_main.text.lower().strip()
                b = self.DCS_logics.list_all_text[self.DCS_logics.index_all_array_sentences[0]]
                # Правильный овтет
                if a == b["2"].lower().strip():
                    if int(b["4"]) < 6:
                        b["4"] = str(int(b["4"]) + 1)
                    # GREAN

                    self.button_send.canvas.before.children[0].rgba = self.Color_True

                # Неправильынй ответ
                else:
                    # Штраф в 3 еденицы
                    if int(b["4"]) >= 3:
                        b["4"] = str(int(b["4"]) - 3)
                        # ELow
                        self.button_send.canvas.before.children[0].rgba = self.Color_Yellow

                    else:
                        b["4"] = str(int(b["4"]) - 1)
                        # READ
                        self.button_send.canvas.before.children[0].rgba = self.Color_False

                    self.label_main.text = '{}\n{}\n{}'.format(
                        self.label_main.text, "- "*len(self.label_main.text), b['2'])

                self.DCS_logics.index_all_array_sentences.pop(0)
                self.trigger = 1

            else:
                self.Next_Word()

        else:
            self.textinput_main.focus = True
            self.Next_Word()
    ############################################################


class zubApp (App):
    icon = r"ico/Zubrila_ico.png"

    def build(self):
        if PLATFORM == 'pc':
            # Размер окна
            Window.size = (500, 700)
            Config.set('graphics', 'resizable', 0)
            # Config.set('graphics', 'fullscreen', 'auto')
            Config.set('kivy', 'exit_on_escape', 1)

        self.layout = Container()
        return self.layout


# Zubrila
if __name__ == "__main__":
    zubApp().run()
