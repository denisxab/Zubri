

"""
Запись работы программы
"""
from datetime import datetime


class CS_Statistics_Bag():
    def __init__(self):
        super(CS_Statistics_Bag, self).__init__()
        self.FILE_NAME = "_Log.txt"

    def Add_Statistics(self, report: str) -> None:
        text = '{} = {}\n'.format(report, datetime.now().strftime("%d-%m-%Y %H:%M"))
        debag = open(self.FILE_NAME, "a", encoding="utf-8").write(text).close()


    def Clear_Report(self) -> None:
        debag_clear = open(self.FILE_NAME, "w").close()




if __name__ == "__main__":
    CS_Statistics_Bag().Add_Statistics("True")
