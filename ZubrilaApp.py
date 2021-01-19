from random import choice, random
from re import findall

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.pagelayout import PageLayout
from kivy.utils import get_color_from_hex



#from kivy.uix.boxlayout import BoxLayout
#from kivy.uix.button import Button
#from kivy.uix.label import Label
#from kivy.uix.scrollview import ScrollView
#from kivy.uix.switch import Switch
#from kivy.uix.textinput import TextInput


from logics import CS_Remember_Logic

# Размер окна
Window.size = (500, 700)
# Потключение виртуальной клавиотуры
Config.set("kivy", "keyboard_mode", "systemanddock")


Color_Background = get_color_from_hex("#3F4F10")
Color_Contant = get_color_from_hex("#6F8072")
Color_Button = get_color_from_hex("#6F8072")


class Container (PageLayout):

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
    # Текстовое поля для ввода флагов
    outputtextflag = ObjectProperty()
    # Флаги выбранные пользователем
    selected_user_flag = []
    # Массив со всеми флагами
    list_flag_json = []
    # Кнопка перелистования на главную страницу
    button_sewap_pagemain = ObjectProperty()
    # Текстовое поля ввода индексов флага
    text_input_flag = ObjectProperty()
    # Виджет - список флагов
    flag_list = ObjectProperty()
    ############################################################

    ############################################################
    # Обнавление кнопок с ответами
    def Refresh_Options(self):

        if self.DCS_logics.index_all_array_sentences:

            chosen = self.DCS_logics.index_all_array_sentences[1::]

            # Если осталься только один варианта ответа
            if len(chosen) < 3:
                b = self.DCS_logics.index_all_array_sentences[0]
                chosen = [b, b, b]

            a = [self.DCS_logics.index_all_array_sentences[0]]

            i = 3
            while i:
                r = choice(chosen)
                a.append(r)
                chosen.remove(r)
                i -= 1

            a = sorted(a, key=lambda A: random())

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
                x.background_color = Color_Button

            if self.DCS_logics.index_all_array_sentences:
                self.label_main.text = self.DCS_logics.list_all_text[
                    self.DCS_logics.index_all_array_sentences[0]]["1"]
                self.label_flag.text = "F({})     L({})".format(
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
                    b["4"] = str(int(b["4"]) + 1)
                    # GREAN
                    ids.background_color = get_color_from_hex("#66D400")

                # Неправильынй ответ
                else:
                    # Штраф в 3 еденицы
                    if int(b["4"]) >= 3:
                        b["4"] = str(int(b["4"]) - 3)
                        # ELow
                        ids.background_color = get_color_from_hex("#D3BD54")

                    else:
                        b["4"] = str(int(b["4"]) - 1)
                        # READ
                        ids.background_color = get_color_from_hex("#D35E54")

                    # Показать кнопку с верныйм ответом

                    for x in self.optionsbutton_list:
                        if x.text == b["2"]:
                            x.background_color = get_color_from_hex("#66D400")

                self.DCS_logics.index_all_array_sentences.pop(0)
                self.trigger = 1

            else:
                New_sentence()

        else:
            New_sentence()

    # Функция переключения способа ответа
    def Switch_Response_Method(self, switchOpj, switchValue):
        #a = self.pagesatting.children[0]
        # On 4 варианта ответ
        if(switchValue):
            self.Show_Options_Response()
        # Off ввод с клавиотуры
        else:
            self.Show_Keyboard_Response()

    # Показать вариант с клавиотурой
    def Show_Keyboard_Response(self):
        # Показать поле ввода и кнопку
        self.boxLayout_keyboard.size_hint_y = 1
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
   
      
        
    def Switch_Order(self, switchOpj, switchValue):
        i = 0
        for x in self.DCS_logics.list_all_text:
            self.DCS_logics.list_all_text[i]['1'],self.DCS_logics.list_all_text[i]['2']  = self.DCS_logics.list_all_text[i]['2'],self.DCS_logics.list_all_text[i]['1']
            i+=1
            



    ############################################################

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
        # !!!
        if not self.selected_user_flag:
            self.button_sewap_pagemain.text = "X"
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
        self.button_sewap_pagemain.text = "<"
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
    def Selekt_Flag(self):
        if self.text_input_flag.text:
            self.selected_user_flag = []
            a = findall(r"\d+", self.text_input_flag.text)
            if a:
                a = list(set(a))

                for x in a:
                    for i in self.list_flag_json:
                        if int(x) == int(i[0]):
                            self.selected_user_flag.append(i[1])

                res = ''
                st = ' '
                for x in self.list_flag_json:
                    st = ' '
                    if str(x[0]) in a:
                        st = '+'

                    res += "{})  {}   [{} : {} : {}]  {}\n".format(
                        x[0], x[1], x[2], x[3], x[4], st)

                self.flag_list.text = res

    # Добовляем флаг
    def Add_Flag(self):
        self.DCS_logics.Add_Flag(self.outputtextflag.text)
        self.DCS_logics.Restart_Data()
        self.outputtextflag.text = ''

    # Отображаем флаги
    def Manager_Flags(self) -> bool:
        # Обновляем список флагов
        self.DCS_logics.Restart_Data()
        self.list_flag_json = self.DCS_logics.Respose_Flag()

        res = ''
        for x in self.list_flag_json:
            res += "{})  {}   [{} : {} : {}]\n".format(
                x[0], x[1], x[2], x[3], x[4])

        self.flag_list.text = res
    ############################################################

    ############################################################
    # Показать новео слово
    def Next_Word(self):

        self.button_send.text = '^'
        self.textinput_main.text = ''
        self.trigger = 0
        self.button_send.background_color = Color_Button

        if self.DCS_logics.index_all_array_sentences:
            self.label_main.text = self.DCS_logics.list_all_text[
                self.DCS_logics.index_all_array_sentences[0]]["1"]
            self.label_flag.text = "F({})     L({})".format(
                self.DCS_logics.list_all_text[self.DCS_logics.index_all_array_sentences[0]]["0"], self.DCS_logics.list_all_text[self.DCS_logics.index_all_array_sentences[0]]["4"])

            # self.Refresh_Options()

        else:
            self.DCS_logics.Save_Result()
            self.DCS_logics.Creating_Array_Sentences()

    # Проверка ответа пользователя
    def Verify_User_Response(self):

        if not self.trigger:

            # Если есть предложения показываем их, и удаляем первое
            if self.DCS_logics.index_all_array_sentences:
                a = self.textinput_main.text.lower().strip()
                b = self.DCS_logics.list_all_text[self.DCS_logics.index_all_array_sentences[0]]
                # Правильный овтет
                if a == b["2"].lower().strip():
                    b["4"] = str(int(b["4"]) + 1)
                    # GREAN
                    self.button_send.background_color = get_color_from_hex(
                        "#66D400")

                # Неправильынй ответ
                else:
                    # Штраф в 3 еденицы
                    if int(b["4"]) >= 3:
                        b["4"] = str(int(b["4"]) - 3)
                        # ELow
                        self.button_send.background_color = get_color_from_hex(
                            "#D3BD54")

                    else:
                        b["4"] = str(int(b["4"]) - 1)
                        # READ
                        self.button_send.background_color = get_color_from_hex(
                            "#D35E54")
                    self.button_send.text = b["2"]

                self.DCS_logics.index_all_array_sentences.pop(0)
                self.trigger = 1

            else:
                self.Next_Word()

        else:
            self.Next_Word()
    ############################################################
    

class ZubrilaApp (App):
    icon = r"ico/Zubrila_32_32.png"
    def build(self):
        self.layout = Container()
        return self.layout

    # Zubrila


if __name__ == "__main__":
    ZubrilaApp().run()
