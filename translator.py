#from selenium import webdriver

#in first version I use selenium
# (dict.cc denied access to Python urllib.request).
# Since I have known how to change user agent
# - selenium is not used in this version of translator.

import re
import os
import requests


class Translator(object):

    def initiate():
        log_path = os.getcwd() + "/settings/log.txt"
        settings_pattern = ["path_of_lists",
                            "is_it_path"]

        if os.path.isfile(log_path):
            with open(log_path, 'r') as log:
                settings = {}
                for line in log:
                    line = line.replace("\n", "")
                    sep = line.find(":")
                    settings[line[:sep]] = line[(sep + 1):len(line)]
                log.close()
            settings2 = {}
            for i in settings_pattern:
                settings2[i] = settings.get(i)
            path_of_lists, is_it_path = map(settings2.get, settings_pattern)
            return path_of_lists, is_it_path

        else: return ""


    def directory_check():
        cont = True
        while cont:
            print ("Where is your directory with list of words?")
            path_of_lists = input()
            while True:
                if not os.path.isdir(path_of_lists):
                    print("You need to write a path ", end="")
                    print ("to the existing directory")
                    break
                else:
                    cont = False
                    break
        return path_of_lists


    def save_settings(self, is_it_path,
                      path_of_lists):
        log_path = os.getcwd() + "/settings/log.txt"
        with open(log_path, 'w') as log:
            log.write("is_it_path:" + str(is_it_path) + "\n")
            log.write("path_of_lists:" + str(path_of_lists))
        log.close()


    def word_list_file(self, path_of_lists):
        print ("Which file do you want to translate?")
        list_of_files = []

        for i in os.listdir(path_of_lists):
            print (os.listdir(path_of_lists).index(i) + 1, i)
            list_of_files.append((os.listdir(path_of_lists).
                                  index(i) + 1, i))

        num_file = input("Check number: ")

        for t in list_of_files:
            i, j = t
            if i == int(num_file):
                print(i)
                words_file = path_of_lists + "/" + j
                break
        return words_file

    def translator(self, is_it_path, path_of_lists):
        print(is_it_path, path_of_lists)
        self.save_settings(is_it_path, path_of_lists)
        plik_ze_slowkami = open(self.word_list_file(path_of_lists), 'r')
        slowka = plik_ze_slowkami.readlines()
        plik_ze_slowkami.close()

        for i in range(0, len(slowka)):
            if "\n" in slowka[i]:
                continue
            else:
                slowka[i] = slowka[i] + "\n"



        basic_url = 'http://www.dict.cc/?s='

        tlumaczenia = []

        SEP = input("""Choose a separator which will delimite words and their translations [e.g. PRESS TAB, ":\"] """)

        print("TRANSLATING...")

        for i in slowka:
            url = basic_url + str(i)
            source = requests.get(url,
                                    headers = {
                                                "User-Agent":
                                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) '
                                               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

                                       }
                                    )

            source = source.text
            if source.find("c1Arr = new Array") > -1:
                s = source.find("c1Arr = new Array") + len("c1Arr = new Array(")
                e = source.find("c2Arr")
                wyniki = source[s:e]
                wyniki = wyniki.split(",")
                i = i[0:i.find("\n")]
                if len(wyniki) >= 3:
                    wyniki = str(i) + SEP \
                             + str(wyniki[1]) + ", " \
                             + str(wyniki[2]) + ", " \
                             + str(wyniki[3])
                elif wyniki < 3:
                    wyniki = str(i) + SEP + str(wyniki[1])
            else:
                continue

            wyniki = wyniki.replace("\"", "")
            tlumaczenia.append(wyniki)


        file = input("Submit name of the file with translated words:")


        file = file + ".txt"

        with open(file, 'w+') as f:
            for line in tlumaczenia:
                print(line)
                f.write(line + "\n")

        return 0
