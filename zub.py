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
    ############################################################
    # Логика программы
    DCS_logics = CS_Remember_Logic()
    ############################################################

    ############################################################
    # Оформление
    Color_Background = get_color_from_hex("#1E4457")
    Color_Contant = get_color_from_hex("#98AEBB")
    Color_True = get_color_from_hex("#66D400")
    Color_False = get_color_from_hex("#D35E54")
    Color_Yellow = get_color_from_hex("#D3BD54")

    Color_Duble = get_color_from_hex("#000000")
    Color_Text_Inpyt = get_color_from_hex("#000000")
    Color_Button = Color_Contant
    Color_Background_Text_Inpyt = Color_Button
    ############################################################

    ############################################################
    # Страница с вопросами
    pagemain = ObjectProperty()
    # Контейнер с <textinput_main> <button_send> <label_flag> <label_main>
    boxLayout_keyboard = ObjectProperty()
    # Бокс со статистикой
    text_statistic_boxlayout = ObjectProperty()
    # Имя флага который показан
    label_flag = ObjectProperty()
    # Кнопка перехода в настройки
    setttings = ObjectProperty()
    # Текстовое поле с вопросом
    label_main = ObjectProperty()
    # Бокс с вопросм
    text_question_boxlayout = ObjectProperty()
    # Текстовое поля для ввода ответа
    textinput_main = ObjectProperty()
    # Болванка для поднятия клавиотуры
    bolvanca_main = ObjectProperty()
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
    # Для переключения предложений
    trigger = 0
    # Порядок показа
    text_display = ['1', '2']
    #-----------------------------------------------------------#
    # Страница с настройками
    pagesatting = ObjectProperty()
    # Мулити кнопка меняющая порядок показа
    switch_revers = ObjectProperty()
    # Мульти кнопка меняющая вариант ответа
    switch_iput = ObjectProperty()
    # Флаги выбранные пользователем
    selected_user_flag = []
    # Массив со всеми флагами
    list_flag_json = []
    # Кнопка перелистования на главную страницу
    button_sewap_pagemain = ObjectProperty()
    # Бокс с флагами
    boxlayout_options_buuton = ObjectProperty()
    # Кнопка перемещения флагов в лево
    left_swap_node = ObjectProperty()
    # Кнопка перемещения флагов в право
    right_swap_node = ObjectProperty()
    # Колличество флагов
    len_flag_label = ObjectProperty()
    # Для перемещения по флагам
    lenger_swap_flag = 0
    #-----------------------------------------------------------#
    # Страница добовления новых слов
    # Кнопка сохраниния флага
    save_flag = ObjectProperty()
    # Текстовое поля для ввода темы
    out_flag_0 = ObjectProperty()
    # Текстовое поля для ввода первого слова
    out_flag_1 = ObjectProperty()
    # Текстовое поля для ввода второго слова
    out_flag_2 = ObjectProperty()
    ############################################################

    imp_data_text = ObjectProperty()
    imp_data_buttun = ObjectProperty()
    output_data_text = ObjectProperty()
    output_data_button = ObjectProperty()

    edit_label_flag = ObjectProperty()
    edit_text_flag = ObjectProperty()
    button_save_edit_flag = ObjectProperty()
    button_del_flag_edit = ObjectProperty()

    ############################################################
    # PAGE 0 Options Button
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
            self.optionsbutton_list[0].text = self.DCS_logics.list_all_text[a[0]
                                                                            ][self.text_display[1]]
            self.optionsbutton_list[1].text = self.DCS_logics.list_all_text[a[1]
                                                                            ][self.text_display[1]]
            self.optionsbutton_list[2].text = self.DCS_logics.list_all_text[a[2]
                                                                            ][self.text_display[1]]
            self.optionsbutton_list[3].text = self.DCS_logics.list_all_text[a[3]
                                                                            ][self.text_display[1]]

    # Проверка отывета пользователя с кнопок

    def Verify_User_Options(self, text, ids):
        def New_sentence():

            self.trigger = 0

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
                # Правильный овтет
                if a == b[self.text_display[1]].lower().strip():
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
                        if x.text == b[self.text_display[1]]:
                            x.canvas.before.children[0].rgba = self.Color_True

                self.DCS_logics.index_all_array_sentences.pop(0)
                self.trigger = 1

            else:
                New_sentence()

        else:
            New_sentence()

    # Функция переключения способа ответа
    def Switch_Response_Method(self, switchValue):
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
        self.text_statistic_boxlayout.size_hint_y = 0.07
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
        self.text_statistic_boxlayout.size_hint_y = 0.1
        self.gridlayout_options_response.size_hint_y = 0.6
        self.gridlayout_options_response.opacity = 1
        self.Refresh_Options()

    # Посенять порядок показа предложений
    def Switch_Order(self, switchValue):

        if switchValue.state == 'down':
            self.text_display[0], self.text_display[1] = self.text_display[1], self.text_display[0]
            return True
        self.text_display[1], self.text_display[0] = self.text_display[0], self.text_display[1]
        return False

    ############################################################
    # Одаптация для телефонов
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
    # Пермещение в приложение
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

    def Impor_Swapig(self):
        #
        self.page = 3

    ############################################################

    ############################################################
    # PAGE 2 Добовление новых слов
    # Добовляем флаг

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

    def Copy_Data_Flags(self):
        if not self.selected_user_flag:
            self.output_data_text.text = ''
            self.output_data_text.hint_text = "Выберети темы для копирывания"
            return False

        res = ''
        for x in self.DCS_logics.list_all_text:
            if x["0"] in self.selected_user_flag:
                res += "0:{}\n1:{}\n2:{}\n4:{}\n~~~\n".format(
                    x["0"], x["1"], x["2"], x["4"])
        self.output_data_text.text = res
        self.output_data_text.hint_text = "Копирывать базу слов(output)\n1) Выберете тему в настройках\n2) Нажмите (?) чтобы получить её копию"
        return True

    def Set_Data_Flags(self):
        if self.DCS_logics.Add_Flag(self.imp_data_text.text):
            self.DCS_logics.Restart_Data()
            self.imp_data_text.text = ''
            self.imp_data_buttun.color = self.Color_Contant
            return True
        else:
            self.imp_data_buttun.color = self.Color_False
            return False

    ############################################################
    # PAGE 1 Flags
    # Конструктор таблицы с флагами
    def __Сreate_Tabel(self):
        return Builder.load_string("""
BoxLayout:
    canvas.before:
        Color:
            rgba: Color_Contant
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [8,]#8

    ToggleButton:
        canvas.before:
            Color:
                rgba: Color_Contant
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [8,]#8
        background_color: 0,0,0,0
        text:"..."
        text_size: self.size
        halign: 'left'
        valign: 'center'
        padding_x: 15
        font_size: '25sp'
        color: Color_Text_Inpyt
        background_normal:''
        background_down:'./ico/green.png'
        on_state:app.layout._Selekt_Flag(self)

    BoxLayout:
        padding:[10,30,10,30]
        orientation: 'vertical'
        size_hint:0.1,1

        Button:
            canvas.before:
                Color:
                    rgba: Color_Background
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [8,]#8
            background_color: 0,0,0,0
            color: Color_Contant
            font_size:'20sp'
            text:'§'
            on_release: app.layout._Setting_Flag(root.children[1])
        
            """)

    # Удаляем весе флаги
    def _Delit_Flag_Edit(self):
        a = findall(r'\d+\)+([^[]+)', self.edit_label_flag.text)[0].strip()
        inde = 0
        le = len(self.DCS_logics.list_all_text)
        while le > 0:
            if self.DCS_logics.list_all_text[inde]['0'] == a:
                self.DCS_logics.list_all_text.pop(inde)
                inde -= 1
            le -= 1
            inde += 1
        self.DCS_logics.Save_Result()
        self.DCS_logics.Restart_Data()
        self.Manager_Flags()
        self.SwapSettings()

    # Переход в настройки флага
    def _Setting_Flag(self, rto):
        # Кнопка удалить весгда красная
        self.button_del_flag_edit.canvas.before.children[0].rgba = self.Color_False
        # Востанавлеваем цвет у кнопки
        self.button_save_edit_flag.canvas.before.children[0].rgba = self.Color_Button
        self.page = 4
        # Получаем текст флага
        self.edit_label_flag.text = rto.text
        # Преабразуем текст для поиска в базе по имени флага
        a = findall(r'\d+\)+([^[]+)', rto.text)[0].strip()
        res = ''
        for x in self.DCS_logics.list_all_text:
            if x["0"] == a:
                res += "0: {}\n1: {}\n2: {}\n4: {}\n~~~\n".format(
                    x["0"], x["1"], x["2"], x["4"])
        self.edit_text_flag.text = res

    # Сохранить результат изменения флага
    def _Save_Edit_Flag(self):
        # Удаляем весе флаги
        self._Delit_Flag_Edit()

        # Сохраняем измененые флаги и обновляем базу
        if self.DCS_logics.Add_Flag(self.edit_text_flag.text):
            self.DCS_logics.Restart_Data()
            self.button_save_edit_flag.canvas.before.children[0].rgba = self.Color_True
            self.Manager_Flags()
            return True
        else:
            self.button_save_edit_flag.canvas.before.children[0].rgba = self.Color_False
            return False

    # Функция для записи флагов. <bind ToggleButton>
    def _Selekt_Flag(self, but_t):
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
        # Отчищаем список выбранных кнопак
        self.selected_user_flag = []
        # Если есть больше 5 элементов то показываем кнопку перемещения вправо
        self.left_swap_node.opacity = 0
        if len(self.list_flag_json) > 5:
            self.right_swap_node.opacity = 1

        # Переменная записывающая положения таблицы
        self.lenger_swap_flag = 0
        # Создаем таблицу
        for x in self.list_flag_json[5*self.lenger_swap_flag:(5*self.lenger_swap_flag)+5:]:
            self.w = self.__Сreate_Tabel()
            self.w.children[1].text = r"{})  {}   [{} : {} : {}]".format(
                x[0], x[1], x[2], x[3], x[4])
            # Решаем проблему отображения выбраннх флагов
            if self.DCS_logics.flags[int(findall(r'(\d+)[)]', self.w.children[1].text)[0])-1][0] in self.selected_user_flag:
                self.w.children[1].state = 'down'
            self.boxlayout_options_buuton.add_widget(self.w)

    #
    # Перелистунть список флагов влево
    def Swap_Left_List_Flag(self):
        # Ограничители передвижения
        if self.lenger_swap_flag-2 < 0:
            self.left_swap_node.opacity = 0
        else:
            self.left_swap_node.opacity = 1

        self.right_swap_node.opacity = 1
        # готовим даннеы для записи
        self.boxlayout_options_buuton.clear_widgets()
        self.boxlayout_options_buuton.canvas.before.children[0].rgba = self.Color_Background
        self.lenger_swap_flag -= 1
        # Состовляем таблицу
        for x in self.list_flag_json[5*self.lenger_swap_flag:(5*self.lenger_swap_flag)+5:]:
            self.w = self.__Сreate_Tabel()
            self.w.children[0].text = r"{})  {}   [{} : {} : {}]".format(
                x[0], x[1], x[2], x[3], x[4])
            if self.DCS_logics.flags[int(findall(r'(\d+)[)]', self.w.children[0].text)[0])-1][0] in self.selected_user_flag:
                self.w.children[0].state = 'down'
            self.boxlayout_options_buuton.add_widget(self.w)
    #
    # Перелистунть список флагов вправо

    def Swap_Right_List_Flag(self):
        # Ограничители передвижения
        if self.lenger_swap_flag+2 > (int(self.len_flag_label.text)-1)//5:
            self.right_swap_node.opacity = 0
        else:
            self.right_swap_node.opacity = 1

        self.left_swap_node.opacity = 1
        # готовим даннеы для записи
        self.boxlayout_options_buuton.clear_widgets()
        self.boxlayout_options_buuton.canvas.before.children[0].rgba = self.Color_Background
        self.lenger_swap_flag += 1
        # Состовляем таблицу
        for x in self.list_flag_json[5*self.lenger_swap_flag:(5*self.lenger_swap_flag)+5:]:
            self.w = self.__Сreate_Tabel()
            self.w.children[0].text = "{})  {}   [{} : {} : {}]".format(
                x[0], x[1], x[2], x[3], x[4])
            if self.DCS_logics.flags[int(findall(r'(\d+)[)]', self.w.children[0].text)[0])-1][0] in self.selected_user_flag:
                self.w.children[0].state = 'down'
            self.boxlayout_options_buuton.add_widget(self.w)

    ############################################################

    ############################################################
    # PAGE 0 Keyboard
    # Показать новео слово

    def Next_Word(self, recus=False):

        self.textinput_main.text = ''
        self.trigger = 0
        self.button_send.canvas.before.children[0].rgba = self.Color_Button

        self.button_send.opacity = 0
        self.button_send.size_hint = (0, 0)
        self.button_send.height = '0'

        if self.DCS_logics.index_all_array_sentences:
            self.label_main.text = self.DCS_logics.list_all_text[
                self.DCS_logics.index_all_array_sentences[0]][self.text_display[0]]

            self.label_flag.text = "{}: {}".format(
                self.DCS_logics.list_all_text[self.DCS_logics.index_all_array_sentences[0]]["0"], self.DCS_logics.list_all_text[self.DCS_logics.index_all_array_sentences[0]]["4"])

        else:
            self.DCS_logics.Save_Result()
            self.DCS_logics.Creating_Array_Sentences()
            if not recus:
                self.Next_Word(True)

    # Сравние сходства двух строчек
    def Line_Similarities(self, str1, str2):
        res = 0.0
        max_similarities = 100/max([len(str1), len(str2)])
        for x, y in zip(str1, str2):
            if x == y:
                res += max_similarities
        return int(round(res, 0))

    # Проверка ответа пользователя

    def Verify_User_Response(self):

        if not self.trigger:
            self.button_send.opacity = 1
            self.button_send.size_hint = (0.1, 1)
            # Если есть предложения показываем их, и удаляем первое
            if self.DCS_logics.index_all_array_sentences:
                a = self.textinput_main.text.lower().strip()
                b = self.DCS_logics.list_all_text[self.DCS_logics.index_all_array_sentences[0]]
                text_user = b[self.text_display[1]].lower().strip()
                # Правильный овтет
                if a == text_user:
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

                    # Отчет об неправильном овтете
                    self.textinput_main.text = ''
                    self.label_main.text = '{}\n{}\n{}\n{}\n{}\n{}%'.format(
                        self.label_main.text, text_user,
                        "- "*len(self.label_main.text),
                        a, "- "*len(self.label_main.text),
                        self.Line_Similarities(text_user, a))

                self.DCS_logics.index_all_array_sentences.pop(0)
                self.trigger = 1

            else:
                self.Next_Word()

        else:
            self.textinput_main.focus = True
            self.Next_Word()
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


# Zubrila
if __name__ == "__main__":
    zubApp().run()
