import re


def string_check(string):
    string = string.replace(' ', '_').lower()
    if str(string) == '':
        return True
    elif not re.match("^[A-Za-z0-9_-]*$", string):
        print("contains bad character")
        print(string)
        return True
    else:
        return False


#def file_motif_search():


def string_to_list(string):
    if type(string) == list:
        return string
    else:
        lst = re.split(r"\n|,", string)
        lst = [x.strip(" ") for x in lst]
        return lst