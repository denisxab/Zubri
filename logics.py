
from re import findall
from datetime import datetime
from Add_Flags import CS_Add_Word


# Чтение файла
class CS_Smooth_Read_File:
    def __init__(self, name_file):
        super(CS_Smooth_Read_File, self).__init__()
        self.report = ''
        self.statis = False
        self.text = self.read_txt(name_file)

    def read_txt(self, name_file: str) -> str:
        try:
            with open(name_file, "r", encoding="utf-8") as all_word:
                try:
                    r_all_word = all_word.read()

                    if r_all_word:
                        self.report = "CS_Read_File - True"
                        self.statis = True

                    else:
                        self.report = "{} empty".format(name_file)
                        self.statis = False
                    return r_all_word

                except UnicodeDecodeError:
                    self.report = "{} UnicodeDecodeError".format(name_file)
                    self.statis = False
                    return ''
        except FileNotFoundError:
            self.report = "{} None".format(name_file)
            self.statis = False
            return ''


# Введение отчета
class CS_Statistics_Bag():
    def __init__(self):
        super(CS_Statistics_Bag, self).__init__()
        self.FILE_NAME = "_Log.txt"

    def Add_Statistics(self, report: str) -> None:
        text = '{} = {}\n'.format(
            report, datetime.now().strftime("%d-%m-%Y %H:%M"))

        with open(self.FILE_NAME, "a", encoding="utf-8") as debag:
            debag.write(text)

    def Clear_Report(self) -> None:
        debag_clear = open(self.FILE_NAME, "w").close()


# Работа с логикой программы
class CS_Remember_Logic():
    ############################################################
    # Конструктор
    def __init__(self):
        super(CS_Remember_Logic, self).__init__()

        self.all_text = ''
        self.flags = []
        self.selected_flags_user = []
        self.index_all_array_sentences = []

        self.Restart_Data()

    # Диструктор
    def __del__(self):
        self.Save_Result()
        return 1
    ############################################################

    # ----------------------- Данные -------------------------------------
    # Сохраниние результат работы

    def Save_Result(self) -> None:
        """
        Сохраниние результат работы <self.list_all_text> в базу <"all_word.txt">
        """
        i = 1
        self.all_text = ''
        for x in self.list_all_text:
            self.all_text += "~{}~\n".format(i)
            i += 1
            for x1 in range(6):
                self.all_text += "{}:{}\n".format(x1, x[str(x1)])
        with open("all_word.txt", "w", encoding="utf-8") as all_word:
            all_word.write(self.all_text)

    # Добавиление слов
    def Add_Flag(self, text_write) -> bool:
        if text_write:
            with open("add_word.txt", "w", encoding="utf-8") as add_word:
                add_word.write(text_write)
            write_new = CS_Add_Word("add_word.txt")


        return True if write_new.Add_Word() else False


    # Обноавить данные
    def Restart_Data(self):

        #------------------------------------------------------------------------------#
        # Весь текст <all_text.txt> в str
        self.all_text = CS_Smooth_Read_File("all_word.txt").text
        #------------------------------------------------------------------------------#

        #------------------------------------------------------------------------------#
        # Запись текста в удобный массив
        self.list_all_text = []
        re_all_text = findall(r"\d:\s*([^~\n]+)", self.all_text)
        for x in range(0, len(re_all_text), 6):
            self.list_all_text.append({
                "0": re_all_text[x],
                "1": re_all_text[x+1],
                "2": re_all_text[x+2],
                "3": re_all_text[x+3],
                "4": re_all_text[x+4],
                "5": re_all_text[x+5]
            })
        del re_all_text
        #------------------------------------------------------------------------------#

        #------------------------------------------------------------------------------#
        # Массив с именем флага и колличество слов с такими флагам и процент знания
        # {'ALL_FLAG': [колличестов_флагов, сумма_всех_4_пунктов, уровень_зания_флага],'Флаг': [2, 7, 3.5]}
        flags = {}
        for x in range(0, len(self.list_all_text)):
            if flags.setdefault(self.list_all_text[x]["0"]):
                flags[self.list_all_text[x]["0"]][0] += 1
                flags[self.list_all_text[x]["0"]
                      ][1] += int(self.list_all_text[x]["4"])
                flags[self.list_all_text[x]["0"]][2] += flags[self.list_all_text[x]
                                                              ["0"]][1] / flags[self.list_all_text[x]["0"]][0]
            else:
                flags[self.list_all_text[x]["0"]] = [
                    1, int(self.list_all_text[x]["4"]), float(self.list_all_text[x]["4"])/1]

        # Переписание <self.flags> в список для навигации по индексам
        self.flags = [[x, flags[x]] for x in flags.keys()]
        #------------------------------------------------------------------------------#

        #------------------------------------------------------------------------------#
        # Выбранные пользователем флаги
        self.selected_flags_user = []
        #------------------------------------------------------------------------------#

        #------------------------------------------------------------------------------#
        # Список идексов всех предложений по выбранным флагам <self.selected_flags_user> после функции <Order_Display> сортируется
        self.index_all_array_sentences = []
    # ----------------------------------------------------------------

    # ------------------ Логика Флагов -------------------------------------
    # Отвечает какие флаги есть в базе
    def Respose_Flag(self):
        # Сортировка 
        res = [[x[0], x[1][0], x[1][1], round(x[1][2])] for x in self.flags]
        res = sorted(res, key=lambda KLK: KLK[1],reverse = True)
        i = 0
        for x in res:
            x.insert(0,i+1)
            i+=1
        return res

    # Запись индексов выбранных флагов
    def Selected_Flags(self, list_flags: list) -> None:
        """
        Запись индексов выбранных флагов
        """



        # Провери выхода за пределы
        for x0 in list_flags:
            if int(x0) > len(self.flags)-1 or int(x0) < 0:
                # LOG WRITE
                CS_Statistics_Bag().Add_Statistics(
                    "All_Text|Selected_Flags|int(x0) > len(self.flags) or int(x0) < 0")
                self.selected_flags_user = []
                return False

        for x in list_flags:
            self.selected_flags_user.append(self.flags[int(x)][0])

        self.selected_flags_user = list(set(self.selected_flags_user))
        return True

    # Составляем список предложений для показа
    def Creating_Array_Sentences(self) -> None:
        """
        Составляем список предложений для показа исходя из <4:>
        """
        self.index_all_array_sentences = []
        iex = 0
        for i0 in self.selected_flags_user:
            iex = 0
            i1 = 0
            for i1 in self.list_all_text:
                if i0 == i1["0"]:
                    self.index_all_array_sentences.append(
                        [int(self.list_all_text[iex]["4"]), iex])
                iex += 1

        self.index_all_array_sentences.sort()
        self.index_all_array_sentences = [x[1]
                                          for x in self.index_all_array_sentences]
    # ----------------------------------------------------------------


def main():
    Remember_Logic = CS_Remember_Logic()
    text = Remember_Logic.Respose_Flag()
    print(text)


if __name__ == "__main__":
    main()
