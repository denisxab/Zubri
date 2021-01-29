from re import match, findall
from datetime import datetime


from Smooth_Read_File import CS_Smooth_Read_File


class CS_Add_Word ():

    def __init__(self, name_input_txt: str) -> None:
        super(CS_Add_Word, self).__init__()

        # Отчет о работе
        self.report = 'CS_Add_Word - True'
        self.statis = True

        # Имя файла с которого считывать - формат .txt
        self.name_input_txt = name_input_txt
        del name_input_txt

        # Запись текста в удобный массив
        self.list_all_text = {}
        re_all_text = findall(
            r"\d:\s*([^~\n]+)", CS_Smooth_Read_File("all_word.txt").text)

        # Количество слов
        self.len_all_list = (len(re_all_text)/6)-1
        for x in range(0, len(re_all_text), 6):
            if not self.list_all_text.get(re_all_text[x]):
                self.list_all_text[re_all_text[x]] = []

            self.list_all_text[re_all_text[x]].append((
                re_all_text[x+1],
                re_all_text[x+2],
                re_all_text[x+3],
                re_all_text[x+4],
                re_all_text[x+5]))

        # for x in range(0, len(re_all_text), 6):
        #     self.list_all_text.append({
        #         "0": re_all_text[x],
        #         "1": re_all_text[x+1],
        #         "2": re_all_text[x+2],
        #         "3": re_all_text[x+3],
        #         "4": re_all_text[x+4],
        #         "5": re_all_text[x+5]
        #     })

        del re_all_text

        # Запись текста в удобный массив
        self.list_add_text = {}

    # Проверка стандарта записи.

    def Document_Verification(self, r_add_word: str) -> bool:
        """
        Проверка правильности заполнения текстового документа <self.name_input_txt>
        """

        # \d:\s*[^~]+ разделить по ~~~
        re_r_add_word = findall(r"\d:\s*[^~]+", r_add_word)

        if not re_r_add_word:
            return False

        # Запись какие пункты есть
        result = []
        for i in re_r_add_word:
            # \d:\s*[^\n]+ разделить по пунктам
            find_re_r_add_word = findall(r"\d:\s*[^\n]+", i)
            result.clear()
            for i1 in find_re_r_add_word:

                # Проверяем и 0 заодно
                if "{0}{1}".format(i1[0], i1[1]) == "0:":
                    result.append(0)

                # Обязательно должны быть пункт 1
                elif "{0}{1}".format(i1[0], i1[1]) == "1:":
                    result.append(1)

                # Обязательно должны быть пункт 2
                elif "{0}{1}".format(i1[0], i1[1]) == "2:":
                    result.append(2)

                # Проверяем и 3 заодно
                elif "{0}{1}".format(i1[0], i1[1]) == "3:":
                    result.append(3)

                # Провереям чтобы в <4:> пункте стояла цифра
                elif "{0}{1}".format(i1[0], i1[1]) == "4:":
                    result.append(4)
                    if not match(r"4:\s*[-\d]+", i1):
                        return False

                # Провереям чтобы в <5:> стаяла дата типа 11.01.2021
                elif "{0}{1}".format(i1[0], i1[1]) == '5:':
                    result.append(5)
                    if not match(r"5:\s*\d+\.\d+\.\d+ \d+:\d+", i1):
                        return False

            # Если нарушен стиль записи то 1 и 2 пункта небудет. А это значит что был нарушен где-то стиль записи
            # возможно поставлен неправильный разделитель и предложение слились в одно.
            # или ненаписали 1 и 2 пункт.
            if not 1 in result or not 2 in result:
                return False

            # Заполняем отсутствующие пункты согласно стандарту
            for i1 in range(1+5-len(result)):
                if not 0 in result:
                    find_re_r_add_word.insert(0, "0: ALL_FLAG")
                    result.append(0)

                elif not 3 in result:
                    find_re_r_add_word.insert(3, "3: NULL_FLAG")
                    result.append(3)

                elif not 4 in result:
                    find_re_r_add_word.insert(4, "4: 0")
                    result.append(4)

                elif not 5 in result:
                    find_re_r_add_word.insert(5, "5: {}".format(
                        datetime.now().strftime("%d.%m.%Y %H:%M")))
                    result.append(5)

            if not self.list_add_text.get(find_re_r_add_word[0][2::].strip()):
                self.list_add_text[find_re_r_add_word[0][2::].strip()] = []

            self.list_add_text[find_re_r_add_word[0][2::].strip()].append((
                find_re_r_add_word[1][2::].strip(),
                find_re_r_add_word[2][2::],
                find_re_r_add_word[3][2::],
                find_re_r_add_word[4][2::],
                find_re_r_add_word[5][2::]))

            # self.list_add_text.append({
            #     "0": find_re_r_add_word[0][2::].strip(),
            #     "1": find_re_r_add_word[1][2::].strip(),
            #     "2": find_re_r_add_word[2][2::],
            #     "3": find_re_r_add_word[3][2::],
            #     "4": find_re_r_add_word[4][2::],
            #     "5": find_re_r_add_word[5][2::]
            # })

        return True

    # Запись <self.name_input_txt> в <all_word.txt>
    def _Add_Word(self) -> bool:
        """
        Дописать в <all_word.txt> предложения из <self.name_input_txt>

        слова в одном и том же флагах недолжные повторяться,
        но могут повторяться в других флагах

        """
        self.add_list = []
        for x in self.list_add_text:
            flag = self.list_all_text.get(x)
            if not flag:
                for y in self.list_add_text[x]:
                    self.add_list.append((x, y[0], y[1], y[2], y[3], y[4]))
            elif flag:
                full_list_all = [q[0] for q in flag]
                for z in self.list_add_text[x]:
                    if not z[0] in full_list_all:
                        self.add_list.append((x, z[0], z[1], z[2], z[3], z[4]))

        if self.add_list:
            with open("all_word.txt", "a", encoding="utf-8") as all_word:
                for x in self.add_list:
                    self.len_all_list += 1
                    a = "~{}~\n0:{}\n1:{}\n2:{}\n3:{}\n4:{}\n5:{}\n".format(
                        int(self.len_all_list),
                        x[0], x[1], x[2], x[3], x[4], x[5])
                    all_word.write(a)
            return True

        return False

        # l_all = [v["1"] for v in self.list_all_text]
        # l_add = [(i, v['0'], v["1"]) for i, v in enumerate(self.list_add_text)]
        # for x in l_add:
        #     if not x[1] in l_all:
        #         self.list_all_text.append(self.list_add_text[x[0]])

        # with open("all_word.txt", "w", encoding="utf-8") as all_word:
        #     i = 0
        #     for x in self.list_all_text:
        #         a = "~{}~\n0:{}\n1:{}\n2:{}\n3:{}\n4:{}\n5:{}\n".format(
        #             i, x["0"], x["1"], x["2"], x["3"], x["4"], x["5"])
        #         all_word.write(a)
        #         i += 1

    # Добавление

    def Add_Word(self):
        """
        Нужно проверить наличие слов в <self.name_input_txt> и проверить их заполнение через функцию Document_Verification(). Предпологаем что <self.name_input_txt> был заполнен зарание, а если он пустой то возвращаем <False>. Если неправильно запомним <self.name_input_txt> (определяем это через <Document_Verification() == False>) то возвращаем <False>. Если правильно заполнен документ проверяем это через <Document_Verification() == True> то записываем (через функцию _Add_Word()()) в <all_word.txt> и возвращаем <True>.

        В конце если запись успешна <_Add_Word()() == True> то отчистить <self.name_input_txt>
        """

        # Проверка заполнения документа <self.name_input_txt>
        if self.Document_Verification(CS_Smooth_Read_File(self.name_input_txt).text) != True:
            # Ошибока в оформление <self.name_input_txt>
            self.report = "{} not  verification".format(self.name_input_txt)
            self.statis = False
            return False

        # Запись
        if self._Add_Word() != True:
            # self.report = self.report - Не удалять
            self.statis = False
            return False

        # Отчистка <self.name_input_txt>
        fcs = open('{}'.format(self.name_input_txt), 'w').close()
        return True


def main():
    write_new = CS_Add_Word("add_word.txt")
    write_new.Add_Word()

    return 1


if __name__ == "__main__":
    main()
