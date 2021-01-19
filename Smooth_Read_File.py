
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
