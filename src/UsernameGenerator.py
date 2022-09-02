import re

class UsernameGenerator:
    def __init__(self, __firstname, __lastname):
        self.firstname = __firstname
        self.lastname = __lastname
        self.possibilities = []
        self.separator=[".","_","-",""]
        self.__generate_username()

    def __get_combo_possibilities(self, __firstname, __lastname, separator):
        return [__firstname+separator+__lastname,__lastname+separator+__firstname]

    def __get_basic_possibilities(self, __firstname, __lastname):
        result=[]
        for sep in self.separator:
            result += self.__get_combo_possibilities(__firstname,__lastname,sep)
        return result

    def __anti_vowel(self, name):
        return re.sub(r'[AEIOUY]', '', name, flags=re.IGNORECASE)

    def __generate_username(self):
        self.possibilities = self.__get_basic_possibilities(self.firstname,self.lastname)
        self.possibilities += self.__get_basic_possibilities(self.firstname,self.__anti_vowel(self.lastname))
        self.possibilities += self.__get_basic_possibilities(self.__anti_vowel(self.firstname),self.lastname)
        self.possibilities += self.__get_basic_possibilities(self.firstname,self.lastname[0])
        self.possibilities += self.__get_basic_possibilities(self.firstname[0],self.lastname)
        self.possibilities += self.__get_basic_possibilities(self.firstname,self.lastname[0:3])
        self.possibilities += self.__get_basic_possibilities(self.firstname[0:3],self.lastname)