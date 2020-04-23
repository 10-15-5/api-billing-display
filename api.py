import requests
import json
import re
import csv
import os


def ahsayAPI_Post(payload, url):
    '''
    Returns a response number of 200 if it successfully connects to the url

    Takes in payload and url as parameters, these are stored as environment variables.
    Uses this payload and url to extract data from the database in JSON format.
    '''
    headers = {'content-type': 'apllication/json'}

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response


def cleanup(r):
    '''
    Returns an list without all the unnecessary commas, apostrophes etc.

    Takes r as a paramter.
    Converts r to a string and then replaces unnecessary punctuation marks.
    Then splits the string and returns it.
    '''
    strR = str(r)
    newstring = (strR.replace('"', '').replace(' ', '').replace("'",
                                        '').replace('{', '').replace('}', '').replace('[','').replace(']', ''))
    arrayList = re.split(':|,', newstring)

    return (arrayList)


def loopThroughData(data):
    '''
    Returns a list that only contains "Login Name", "Owner", "Quota Used" and "Quota".

    Takes in the arraylist that was cleaned up in the previous function.
    Loops through the data and every time it comes across one of the key words, it appends the next item to the end of the new list.
    I ran into a problem where a zero was being printed in the "Login Name" column.
    I coded in a validation process whereby it always checks to see if the value before "Login Name" is zero, if so it gets deleted.
    The "Quota" and "Quota Used" were in bytes so I had to change them to terabytes.
    '''
    list = []

    for item in range(len(data)):
        if data[item] == 'LoginName':
            list.append(data[item + 1])
            x = (len(list) - 2)
            if list[x] == 0:
                del list[x]
        elif data[item] == 'Owner':
            list.append(data[item + 1])
        elif data[item] == 'DataSize':
            byte = int(data[item + 1])
            tera = byte / (1024 ** 4)
            list.append(tera)
        elif data[item] == 'Quota':
            byte = int(data[item + 1])
            tera = byte / (1024 ** 4)
            list.append(tera)

    return list


def reorderheadings(list):
    '''
    Returns a new list with the members of the old list in a different order ("Owner", "Login Name", "Quota", "Quota Used")

    I wanted the list to display in the csv in a differnet order.
    This function takes the list in groups of 4 and reorders them to the order I've specified.
    '''

    newlist = []

    for index in range(0, len(list) - 1, 4):
        start = index
        loginname = list[start]
        owner = list[start + 1]
        quotaused = list[start + 2]
        quota = list[start + 3]

        newlist.append([owner, loginname, quotaused, quota])

    newlist.sort(key=lambda newlist: newlist[0])
    newlist2 = cleanup(newlist)

    newlist2.insert(0, 'OWNER')
    newlist2.insert(1, 'LOGIN NAME')
    newlist2.insert(2, 'QUOTA USED')
    newlist2.insert(3, 'QUOTA')


    return newlist2


def writeToFile(list):
    '''
    Prints the list to a csv file.

    Takes the first 4 items, prints them and then adds a line break to move to the next line and start again on the next 4 items in the list.
    This function is in a try; except block as the code would crash if the user hadthe csv file already open on their machine.
    '''
    counter = 1;
    value_to_write = ''
    file = 'api.csv'

    try:
        with open(file, 'w') as file:

            for item in list:
                if counter == 4:  # adds line break after every 3rd item
                    value_to_write = f"{item}\n"
                    counter = 1  # resets counter to 1 after every third item
                else:  # adds comma if not adding line break
                    value_to_write = f"{item},"
                    counter += 1
                file.write(value_to_write)  # writes to file
            print("Let's hope this works!")

    except IOError:
        print('ERROR WRITING TO FILE:		Please close "' + file + '" before you run this program!')
    except FileNotFoundError:
        print('FILE NOT FOUND ERROR:		Please create a file called: "' + file + '" before you run this program!')


def envrion_login_details():
    '''
    Returns the API Login details and the API URL details that I have set up as environment variables.
    '''
    login = os.environ.get('API_LOGIN')
    url = os.environ.get('API_URL')

    login_dict = json.loads(login)

    return login_dict, url


login, url = envrion_login_details()

r = ahsayAPI_Post(login, url)

arrayList = cleanup(r.json())

list = loopThroughData(arrayList)

newlist = reorderheadings(list)

writeToFile(newlist)
