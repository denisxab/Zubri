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
# Подключение виртуальной клавиатуры
Config.set("kivy", "keyboard_mode", "systemanddock")


# Операционная система
# pc | phone
PLATFORM = 'phone'


class Container (PageLayout):
    ############################################################
    # Логика программы
    DCS_logics = CS_Remember_Logic()
    ############################################################

    ############################################################
    # Оформление
    Color_Background = get_color_from_hex("#1E4457")
    Color_Content = get_color_from_hex("#98AEBB")
    Color_True = get_color_from_hex("#66D400")
    Color_False = get_color_from_hex("#D35E54")
    Color_Yellow = get_color_from_hex("#D3BD54")

    Color_Double = get_color_from_hex("#000000")
    Color_Text_Input = get_color_from_hex("#000000")
    Color_Button = Color_Content
    Color_Background_Text_Input = Color_Button
    ############################################################

    ############################################################
    # Страница с вопросами
    page_main = ObjectProperty()
    # Контейнер с <text_input_main> <button_send> <label_flag> <label_main>
    box_Layout_keyboard = ObjectProperty()
    # Бокс со статистикой
    text_statistic_box_layout = ObjectProperty()
    # Имя флага который показан
    label_flag = ObjectProperty()
    # Кнопка перехода в настройки
    settings = ObjectProperty()
    # Текстовое поле с вопросом
    label_main = ObjectProperty()
    # Бокс с вопросом
    text_question_box_layout = ObjectProperty()
    # Текстовое поля для ввода ответа
    text_input_main = ObjectProperty()
    # Болванка для поднятия клавиатуры
    blank_main = ObjectProperty()
    # Кнопка - отправить результат с клавиатуры
    button_send = ObjectProperty()

    # Контейнер с кнопками ответов
    gridlayout_options_response = ObjectProperty()
    # Кнопки в выбором ответа
    butt_send10 = ObjectProperty()
    butt_send20 = ObjectProperty()
    butt_send30 = ObjectProperty()
    butt_send40 = ObjectProperty()
    optionsbutton_list = []
    # Для переключения предложений
    trigger = 0
    # Порядок показа
    text_display = ['1', '2']
    #-----------------------------------------------------------#
    # Страница с настройками
    page_setting = ObjectProperty()
    # Мульт кнопка меняющая порядок показа
    switch_revers = ObjectProperty()
    # Мульт кнопка меняющая вариант ответа
    switch_input = ObjectProperty()
    # Флаги выбранные пользователем
    selected_user_flag = []
    # Массив со всеми флагами
    list_flag_json = []
    # Кнопка перелистования на главную страницу
    button_swap_page_main = ObjectProperty()
    # Бокс с флагами
    box_layout_options_button = ObjectProperty()
    # Кнопка перемещения флагов в лево
    left_swap_node = ObjectProperty()
    # Кнопка перемещения флагов в право
    right_swap_node = ObjectProperty()
    # Количество флагов
    len_flag_label = ObjectProperty()
    # Для перемещения по флагам
    lenger_swap_flag = 0
    #-----------------------------------------------------------#
    # Страница добавления новых слов
    # Кнопка сохранения флага
    save_flag = ObjectProperty()
    # Текстовое поля для ввода темы
    out_flag_0 = ObjectProperty()
    # Текстовое поля для ввода первого слова
    out_flag_1 = ObjectProperty()
    # Текстовое поля для ввода второго слова
    out_flag_2 = ObjectProperty()
    ############################################################

    imp_data_text = ObjectProperty()
    imp_data_button = ObjectProperty()
    output_data_text = ObjectProperty()
    output_data_button = ObjectProperty()

    edit_text_input_flag = ObjectProperty()
    edit_text_flag = ObjectProperty()
    button_save_edit_flag = ObjectProperty()
    button_del_flag_edit = ObjectProperty()

    helper_user_button = ObjectProperty()

    rename_flag_button = ObjectProperty()
    # Переменная для хранения имени редактируемого флага
    main_edit_flag = ''

    add_chosen_flag_button = ObjectProperty()
    box_helper = ObjectProperty()

    all_table = []

    ############################################################
    # PAGE 0 Options Button
    # Обновление кнопок с ответами

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
            self.optionsbutton_list[0].text = self.DCS_logics.list_all_text[a[0]
                                                                            ][self.text_display[1]]
            self.optionsbutton_list[1].text = self.DCS_logics.list_all_text[a[1]
                                                                            ][self.text_display[1]]
            self.optionsbutton_list[2].text = self.DCS_logics.list_all_text[a[2]
                                                                            ][self.text_display[1]]
            self.optionsbutton_list[3].text = self.DCS_logics.list_all_text[a[3]
                                                                            ][self.text_display[1]]
    #
    #
    # Проверка ответа пользователя с кнопок

    def Verify_User_Options(self, text, ids):
        def New_sentence():

            self.trigger = 0
            self.add_chosen_flag_button.background_normal = "./ico/like.png"
            for x in self.optionsbutton_list:
                x.canvas.before.children[0].rgba = self.Color_Button

            if self.DCS_logics.index_all_array_sentences:
                self.label_main.text = self.DCS_logics.list_all_text[
                    self.DCS_logics.index_all_array_sentences[0]][self.text_display[0]]
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
                # Правильный ответ
                if a == b[self.text_display[1]].lower().strip():
                    if int(b["4"]) < 6:
                        b["4"] = str(int(b["4"]) + 1)
                    # GREEN
                    ids.canvas.before.children[0].rgba = self.Color_True

                # Неправильный ответ
                else:
                    # Штраф в 3 единицы
                    if int(b["4"]) >= 3:
                        b["4"] = str(int(b["4"]) - 3)
                        # ELow
                        ids.canvas.before.children[0].rgba = self.Color_Yellow

                    else:
                        b["4"] = str(int(b["4"]) - 1)
                        # READ
                        ids.canvas.before.children[0].rgba = self.Color_False

                    # Показать кнопку с верными ответом

                    for x in self.optionsbutton_list:
                        if x.text == b[self.text_display[1]]:
                            x.canvas.before.children[0].rgba = self.Color_True

                self.DCS_logics.index_all_array_sentences.pop(0)
                self.trigger = 1

            else:
                New_sentence()

        else:
            New_sentence()
    #
    #
    # Функция переключения способа ответа

    def Switch_Response_Method(self, switchValue):
        # On 4 варианта ответ
        if switchValue.state == "down":
            self.Show_Options_Response()
        # Off ввод с клавиатуры
        else:

            self.Show_Keyboard_Response()
    #
    #
    # Показать вариант с клавиатуры

    def Show_Keyboard_Response(self):
        # Показать поле ввода и кнопку
        self.box_Layout_keyboard.size_hint_y = 0.1
        self.box_Layout_keyboard.opacity = 1
        # Скрыть кнопки ответов, они должны уменьшаться чтобы невылазить
        self.text_statistic_box_layout.size_hint_y = 0.07
        self.gridlayout_options_response.opacity = 0
        self.gridlayout_options_response.size_hint_y = None
        self.gridlayout_options_response.height = '0'
        # Корректировать размер бокса с добавление в изубранное
        self.box_helper.size_hint_y = 0.15
        self.Next_Word()
    #
    #
    # Показать вариант с кнопками

    def Show_Options_Response(self):
        # Скрыть поле ввода и кнопку
        self.box_Layout_keyboard.size_hint_y = 0.1
        self.box_Layout_keyboard.opacity = 0
        # Отчистка поля ввода
        self.text_input_main.text = ""
        # Показать кнопки ответов, они должны уменьшаться чтобы невылазить
        self.text_statistic_box_layout.size_hint_y = 0.1
        self.gridlayout_options_response.size_hint_y = 0.6
        self.gridlayout_options_response.opacity = 1
        # Корректировать размер бокса с добавление в изубранное
        self.box_helper.size_hint_y = 0.3
        self.Refresh_Options()

    #
    #
    # Поменять порядок показа предложений

    def Switch_Order(self, switchValue):
        if switchValue.state == 'down':
            self.text_display[0], self.text_display[1] = self.text_display[1], self.text_display[0]
            return True
        self.text_display[1], self.text_display[0] = self.text_display[0], self.text_display[1]
        return False

        ############################################################

    ############################################################
    # PAGE 0 Keyboard
    # Подсказка

    def Help_User_Main(self, vis=0):
        # На случай если пользователь захочет нажать подсказку когда уже есть ответ
        if not self.trigger:
            a = self.DCS_logics.list_all_text[self.DCS_logics.index_all_array_sentences[0]]
            if not vis:
                self.label_main.text = '{}\n{}'.format(
                    a[self.text_display[0]],
                    a[self.text_display[1]])
            else:
                self.label_main.text = a[self.text_display[0]]

    #
    #
    # Добавить в избранные

    def Add_Chosen_Flag(self):

        self.add_chosen_flag_button.background_normal = "./ico/like_touch.png"
        a = self.DCS_logics.list_all_text[self.DCS_logics.index_all_array_sentences[0]]

        outputtextflag = '0:{}\n1:{}\n2:{}\n'.format(
            "Избранное", a['1'], a['2'])
        self.DCS_logics.Add_Flag(outputtextflag)

        # Это костыль но так надежнее
        tmp = self.DCS_logics.index_all_array_sentences
        self.DCS_logics.Restart_Data()
        self.DCS_logics.index_all_array_sentences = tmp

    #
    # Показать новые слово

    def Next_Word(self, recuse=False):
        # Текстовое поле дял ввода отчистить
        self.text_input_main.text = ''
        # Тригер в исходное
        self.trigger = 0
        # Картинку избранного в исходное
        self.add_chosen_flag_button.background_normal = "./ico/like.png"
        # Спрятать кнопку ответа
        self.button_send.opacity = 0
        self.button_send.size_hint = (0, 0)
        self.button_send.height = '0'
        # Цвет кнопки ответа в исходное
        self.button_send.canvas.before.children[0].rgba = self.Color_Button

        if self.DCS_logics.index_all_array_sentences:
            a = self.DCS_logics.list_all_text[self.DCS_logics.index_all_array_sentences[0]]
            self.label_main.text = a[self.text_display[0]]
            self.label_flag.text = "{}: {}".format(a["0"], a["4"])

            if int(a["4"]) < 1:
                self.helper_user_button.background_normal = "./ico/help.png"
                self.helper_user_button.background_down = "./ico/help_touch.png"
                self.helper_user_button.on_release = lambda: self.Help_User_Main(
                    False)

            else:
                self.helper_user_button.background_normal = ''
                self.helper_user_button.background_down = ''
                self.helper_user_button.on_release = lambda: self.Help_User_Main(
                    True)

        else:
            self.DCS_logics.Save_Result()
            self.DCS_logics.Creating_Array_Sentences()
            if not recuse:
                self.Next_Word(True)
    #
    #
    # Проверка ответа пользователя

    def Verify_User_Response(self):
        # Сравнение сходства двух строчек
        def Line_Similarities(str1, str2):
            res = 0.0
            max_similarities = 100/max([len(str1), len(str2)])
            for x, y in zip(str1, str2):
                if x == y:
                    res += max_similarities
            return int(round(res, 0))

        if not self.trigger:
            self.button_send.opacity = 1
            self.button_send.size_hint = (0.1, 1)
            # Если есть предложения показываем их, и удаляем первое
            if self.DCS_logics.index_all_array_sentences:
                a = self.text_input_main.text.lower().strip()
                b = self.DCS_logics.list_all_text[self.DCS_logics.index_all_array_sentences[0]]
                text_user = b[self.text_display[1]].lower().strip()
                # Правильный ответ
                if a == text_user:
                    if int(b["4"]) < 6:
                        b["4"] = str(int(b["4"]) + 1)
                    # GREEN

                    self.button_send.canvas.before.children[0].rgba = self.Color_True

                # Неправильный ответ
                else:
                    # Штраф в 3 едениц
                    if int(b["4"]) >= 3:
                        b["4"] = str(int(b["4"]) - 3)
                        # ELow
                        self.button_send.canvas.before.children[0].rgba = self.Color_Yellow

                    else:
                        b["4"] = str(int(b["4"]) - 1)
                        # READ
                        self.button_send.canvas.before.children[0].rgba = self.Color_False

                    # Отчет об неправильном ответ
                    self.text_input_main.text = ''
                    self.label_main.text = ''

                    self.label_main.text = '{}\n{}\n{}\n{} - {}%'.format(
                        b[self.text_display[0]], text_user,
                        "- "*len(text_user), a,
                        Line_Similarities(text_user, a))

                self.DCS_logics.index_all_array_sentences.pop(0)
                self.trigger = 1

            else:
                self.Next_Word()

        else:
            self.text_input_main.focus = True
            self.Next_Word()
    ############################################################

    ############################################################
    # Адаптация для телефонов
    # Поднятие клавиатуры в на главной старанице

    def Text_Input_Response_on_focus(self, value):
        if PLATFORM == "phone":
            if value:
                self.blank_main.size_hint_y = 0.4

                self.box_helper.size_hint_y = 0.45
                self.text_statistic_box_layout.size_hint_y = 0.0625
                self.text_question_box_layout.size_hint_y = 0.3
                self.box_Layout_keyboard.size_hint_y = 0.1

            else:
                self.blank_main.size_hint_y = None
                self.blank_main.height = '0'

                self.box_helper.size_hint_y = 0.15
                self.text_statistic_box_layout.size_hint_y = 0.07
                self.text_question_box_layout.size_hint_y = 0.8
                self.box_Layout_keyboard.size_hint_y = 0.1

        # Убирает текст подсказки когда фокус на клавиатуре
        if value and self.text_input_main.text == '' and self.DCS_logics.index_all_array_sentences:
            self.Help_User_Main(1)

        if not value and self.text_input_main.text != '':
            self.Verify_User_Response()
    ############################################################

    ############################################################
    # Перемещение в приложение
    # Переключиться в Настройки из главной страницы

    def Swap_Settings(self):
        # Сохраняем результат ответов
        self.DCS_logics.Save_Result()
        # Переключаемся в настройки
        self.page = 1
    #
    #
    # Переключиться на главную страницу из настройки

    def Swap_Page_Main(self):
        # Если флаги не выбраны то не переходим на главную страницу
        if not self.selected_user_flag:
            self.button_swap_page_main.background_down = './ico/Qarrow_L.png'
            self.button_swap_page_main.canvas.before.children[0].rgba = self.Color_False
            return False

        self.DCS_logics.Save_Result()
        # Конвертируем значения из таблицы
        self.DCS_logics.selected_flags_user = self.selected_user_flag

        # Создаем список предложений
        self.DCS_logics.Creating_Array_Sentences()
        # Показываем предложение
        self.Next_Word()

        #!!! На сулачай если перейти из главного окна в настройки при вариативном ответе
        self.Refresh_Options()

        # Скрываем кнопку помощи
        if self.switch_input.state == "down":
            self.helper_user_button.background_normal = ''
            self.helper_user_button.background_down = ''
            self.helper_user_button.on_release = lambda: self.Help_User_Main(
                True)

        # Скидываем цвет кнопку в исходный
        self.button_swap_page_main.background_down = './ico/Qarrow_R.png'
        self.button_swap_page_main.canvas.before.children[0].rgba = self.Color_Button
        # Переключаемся на главный слой
        self.page = 0

        return True
    #
    #
    # Переключаемся на страницу добавление предложений из настройки

    def Swap_Write_Flags(self):
        #
        self.page = 2
    #
    #
    # Переключаемся на в настройки из добавления предложений

    def Settings_SwapWriteFlags(self):
        #
        self.page = 1
    #
    #

    def Import_Swapping(self):
        #
        self.page = 3
    ############################################################

    ############################################################
    # PAGE 2 Добавление новых слов
    # Добавляем флаг

    def Add_Flag(self):

        if self.out_flag_0.text and self.out_flag_1.text and self.out_flag_2.text:
            outputtextflag = '0:{}\n1:{}\n2:{}\n'.format(self.out_flag_0.text,
                                                         self.out_flag_1.text,
                                                         self.out_flag_2.text)
            if self.DCS_logics.Add_Flag(outputtextflag):
                self.DCS_logics.Restart_Data()
                # self.out_flag_0.text = ''
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
    #
    #

    def Copy_Data_Flags(self):
        if not self.selected_user_flag:
            self.output_data_text.text = ''
            self.output_data_text.hint_text = "Выберете темы для копирывания"
            return False

        res = ''
        for x in self.DCS_logics.list_all_text:
            if x["0"] in self.selected_user_flag:
                res += "0:{}\n1:{}\n2:{}\n4:{}\n~~~\n".format(
                    x["0"], x["1"], x["2"], x["4"])
        self.output_data_text.text = res
        self.output_data_text.hint_text = "Копирывать базу слов(output)\n1) Выберете тему в настройках\n2) Нажмите (?) чтобы получить её копию"
        return True
    #
    #

    def Set_Data_Flags(self):
        if self.DCS_logics.Add_Flag(self.imp_data_text.text):
            self.DCS_logics.Restart_Data()
            self.imp_data_text.text = ''
            self.imp_data_button.color = self.Color_Content
            return True
        else:
            self.imp_data_button.color = self.Color_False
            return False
    ############################################################
    # PAGE 1 Flags
    #
    # Переименовать флаг

    def _Rename_Flag(self, text_flag: str):

        for x in self.DCS_logics.list_all_text:
            if x['0'] == self.main_edit_flag:
                x['0'] = text_flag
        self.Swap_Settings()
        self.Manager_Flags()

    #
    #
    # Удаляем весе флаги

    def _Delete_Flag_Edit(self):
        index = 0
        le = len(self.DCS_logics.list_all_text)
        while le > 0:
            if self.DCS_logics.list_all_text[index]['0'] == self.main_edit_flag:
                self.DCS_logics.list_all_text.pop(index)
                index -= 1
            le -= 1
            index += 1
        self.DCS_logics.Save_Result()
        self.DCS_logics.Restart_Data()
        self.Swap_Settings()
        self.Manager_Flags()
    #
    #
    # Переход в настройки флага

    def _Setting_Flag(self, rto):
        # Кнопка удалить всегда красная
        self.button_del_flag_edit.canvas.before.children[0].rgba = self.Color_False
        # Восстанавливаем цвет у кнопки
        self.button_save_edit_flag.canvas.before.children[0].rgba = self.Color_Button
        # Кнопка переименовать желтого цвета
        self.rename_flag_button.canvas.before.children[0].rgba = self.Color_Yellow
        # Переключиться на 4 страницу
        self.page = 4
        # Получаем текст флага
        self.main_edit_flag = findall(r'\d+\)+([^[]+)', rto.text)[0].strip()
        # Записываем его в текстовое поле
        self.edit_text_input_flag.text = self.main_edit_flag
        res = ''
        for x in self.DCS_logics.list_all_text:
            if x["0"] == self.main_edit_flag:
                res += "0: {}\n1: {}\n2: {}\n4: {}\n~~~\n".format(
                    x["0"], x["1"], x["2"], x["4"])
        self.edit_text_flag.text = res
    #
    #
    # Сохранить результат изменения флага

    def _Save_Edit_Flag(self):
        # Удаляем весе флаги
        index = 0
        le = len(self.DCS_logics.list_all_text)
        while le > 0:
            if self.DCS_logics.list_all_text[index]['0'] == self.main_edit_flag:
                self.DCS_logics.list_all_text.pop(index)
                index -= 1
            le -= 1
            index += 1
        self.DCS_logics.Save_Result()

        # Сохраняем измененные флаги и обновляем базу
        if self.DCS_logics.Add_Flag(self.edit_text_flag.text):
            self.DCS_logics.Restart_Data()
            self.Swap_Settings()
            self.Manager_Flags()
            return True
        else:
            self.button_save_edit_flag.canvas.before.children[0].rgba = self.Color_False
            return False
    #
    #
    # Функция для записи флагов. <bind ToggleButton>

    def _Select_Flag(self, but_t):
        # Записываем нажатые флаги в массив, для дальнейше обработки
        self.selected_user_flag = list(set(self.selected_user_flag))
        a = findall(r'\d+\)+([^[]+)', but_t.text)[0].strip()
        if but_t.state == 'down':
            if a in [x[0]for x in self.DCS_logics.flags]:
                self.selected_user_flag.append(a)
                but_t.canvas.before.children[0].rgba = self.Color_True
                return True
        self.selected_user_flag.remove(a)
        but_t.canvas.before.children[0].rgba = self.Color_Button
        return False
    #
    #
    # Обновить список флагов

    def Manager_Flags(self) -> bool:
        # Получаем флаги из базы
        self.list_flag_json = self.DCS_logics.Respose_Flag()
        # Максималья длинна флага
        self.len_flag_label.text = str(len(self.list_flag_json))
        # Переменная с помощью которой определяем пределы
        self.lenger_swap_flag = 0
        # Отчистка поля с флагами
        self.box_layout_options_button.clear_widgets()
        self.box_layout_options_button.canvas.before.children[0].rgba = self.Color_Background
        # Если есть больше 5 элементов то показываем кнопку перемещения вправо
        self.right_swap_node.opacity = 0
        self.left_swap_node.opacity = 0
        if len(self.list_flag_json) > 5:
            self.right_swap_node.opacity = 1
            self.right_swap_node.size_hint_y = 1

        if not self.all_table:
            # Отчищаем список выбранных кнопка
            self.selected_user_flag = []
            # Создаем массив со всеми возможными кнопками
            for x in self.list_flag_json:
                w = Builder.load_file('table.kv')
                w.children[1].text = r"{})  {}   [{} : {} : {}]".format(
                    x[0], x[1], x[2], x[3], x[4])
                self.all_table.append(w)
        else:
            # Отчищаем список выбранных кнопка
            for x in self.all_table:
                x.children[1].state = 'normal'
                x.canvas.before.children[0].rgba = self.Color_Button

            # При добавление новых флагов
            if len(self.all_table) < len(self.list_flag_json):
                flg = [findall(r'\d+\)+([^[]+)', x.children[1].text)
                       [0].strip() for x in self.all_table]
                for x in self.list_flag_json:
                    if not x[1] in flg:
                        w = Builder.load_file('table.kv')
                        w.children[1].text = r"{})  {}   [{} : {} : {}]".format(
                            x[0], x[1], x[2], x[3], x[4])
                        self.all_table.append(w)

            # При удаление флага
            elif len(self.all_table) > len(self.list_flag_json):
                for x in self.all_table:
                    if not findall(r'\d+\)+([^[]+)', x.children[1].text)[0].strip() in [x[1] for x in self.list_flag_json]:
                        x.clear_widgets()
                        self.all_table.remove(x)

            # На случай если будут переименованны флаги
            else:
                for y, x in zip(self.all_table, self.list_flag_json):
                    y.children[1].text = r"{})  {}   [{} : {} : {}]".format(
                        x[0], x[1], x[2], x[3], x[4])

        # Показываем первые 5 тем
        for x in self.all_table[5*self.lenger_swap_flag:5*self.lenger_swap_flag+5:]:
            self.box_layout_options_button.add_widget(x)

    #
    #
    # Перелистнуть список флагов влево

    def Swap_Left_List_Flag(self):
        # Ограничители передвижения
        if self.lenger_swap_flag-2 < 0:
            self.left_swap_node.opacity = 0
            self.left_swap_node.size_hint_y = None
            self.left_swap_node.height = '0'

        else:
            self.left_swap_node.opacity = 1
            self.left_swap_node.size_hint_y = 1

        self.right_swap_node.opacity = 1
        self.right_swap_node.size_hint_y = 1
        # готовим данные для записи
        self.box_layout_options_button.clear_widgets()
        self.box_layout_options_button.canvas.before.children[0].rgba = self.Color_Background
        self.lenger_swap_flag -= 1

        for x in self.all_table[5*self.lenger_swap_flag:5*self.lenger_swap_flag+5:]:
            self.box_layout_options_button.add_widget(x)

    #
    #
    # Перелистнуть список флагов вправо

    def Swap_Right_List_Flag(self):
        # Ограничители передвижения
        if self.lenger_swap_flag+2 > (len(self.list_flag_json)-1)//5:
            self.right_swap_node.opacity = 0
            self.right_swap_node.size_hint_y = None
            self.right_swap_node.height = '0'
        else:
            self.right_swap_node.opacity = 1
            self.right_swap_node.size_hint_y = 1

        self.left_swap_node.opacity = 1
        self.left_swap_node.size_hint_y = 1

        # готовим данные для записи
        self.box_layout_options_button.clear_widgets()
        self.box_layout_options_button.canvas.before.children[0].rgba = self.Color_Background
        self.lenger_swap_flag += 1

        for x in self.all_table[5*self.lenger_swap_flag:5*self.lenger_swap_flag+5:]:
            self.box_layout_options_button.add_widget(x)

    ############################################################


class zubApp (App):
    icon = r"ico/Zubri_ico.png"

    def build(self):
        if PLATFORM == 'pc':
            # Размер окна
            Window.size = (500, 700)
            Config.set('graphics', 'resizable', 0)
            # Config.set('graphics', 'fullscreen', 'auto')
            Config.set('kivy', 'exit_on_escape', 1)

        self.layout = Container()
        return self.layout


# Zubri
if __name__ == "__main__":
    zubApp().run()
