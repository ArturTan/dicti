import os
from translator import Translator as T


print ("Hello, this program will help you "
       "in creating tables \nof translations of German"
       " words to English equivalents.\n", sep="")

path_of_lists, is_it_path = T.initiate()

while True:
    if is_it_path:
        print("This is your previous list directory:\n", path_of_lists,
              "\n\nDo you want to change your directory? (y/n)", sep="")
        answer = input()
        if answer == "n":
            break
        elif answer == 'y':
            path_of_lists = T.directory_check()
            is_it_path = True
            break
        else:
            continue
    else:
        path_of_lists = t.directory_check()
        is_it_path = True
        break

print(is_it_path, path_of_lists)

x = T()

x.translator(is_it_path, path_of_lists)




