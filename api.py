import requests
import json
import re
import csv
import os


def ahsayAPI_Post(payload, url):
	headers 	= 	{'content-type':'apllication/json'}

	response = requests.post(url, data=json.dumps(payload), headers=headers)
	return response


def cleanup(r):
	strR = str(r)
	newString = (strR.replace('"', '').replace(' ', '').replace("'", '').replace('{','').replace('}',''))
	arrayList = re.split(':|,', newString)
	
	return(arrayList)


def loopThroughData(data):
	list = []
	list.append('LOGIN NAME')
	list.append('OWNER')
	list.append('QUOTA USED')
	list.append('QUOTA')
	
	for item in range(len(data)):
		if data[item] == 'LoginName':
			list.append(data[item+1])
			x = (len(list) - 2)
			if list[x] == 0:
				del list[x]
		elif data[item] == 'Owner':
			list.append(data[item+1])
		elif data[item] == 'DataSize':
			byte = int(data[item+1])
			tera = byte / (1024**4)
			list.append(tera)
		elif data[item] == 'Quota':
			byte = int(data[item+1])
			tera = byte / (1024**4)
			list.append(tera)
			
	return list
	
	
def reorderheadings(list):
	
	newlist = []
	
	for index in range(0, len(list) - 1, 4):
		start = index
		end = start + 4
		
		newlist.append(list[start+1])
		newlist.append(list[start])
		newlist.append(list[start+3])
		newlist.append(list[start+2])
		

	return newlist


def writeToFile(list):
	counter = 1;
	value_to_write = ''
	file = 'api.csv'
	
	try:
		with open(file, 'w') as file:
		
			for item in list:
				if counter == 4:															#adds line break after every 3rd item
					value_to_write = f"{item}\n"
					counter = 1 															#resets counter to 1 after every third item
				else: 																		#adds comma if not adding line break
					value_to_write = f"{item},"
					counter += 1	
				file.write(value_to_write)													#writes to file
			print("Let's hope this works!")

	except IOError:
		print('ERROR WRITING TO FILE:		Please close "' + file + '" before you run this program!')
	except FileNotFoundError:
		print('FILE NOT FOUND ERROR:		Please create a file called: "' + file + '" before you run this program!')


def envrion_login_details():
	login = os.environ.get('API_LOGIN')
	url = os.environ.get('API_URL')
	
	login_dict = json.loads(login)
	
	return login_dict, url


login, url			= envrion_login_details()

r 				= ahsayAPI_Post(login, url)

arrayList 		= cleanup(r.json())

list 			= loopThroughData(arrayList)

newlist 		= reorderheadings(list)

writeToFile(newlist)
