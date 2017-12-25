import shutil
import os
import getpass

def read_settings():
	settings_lijst = []
	read_settings_file = open('settings.txt', 'r')
	settings_lijst = read_settings_file.readlines()
	read_settings_file.close()
	return settings_lijst
# einde read_settings def

def update_settings(): #funcite waarmee de admin de huidige informatie kan aanpassen
	settings_lijst = []
	username = input("Username: ")
	wachtwoord = input("Wachtwoord: ")
	login_credentials = username + ";" + wachtwoord + "\n"
	login_status = "failed"
	type_of_copy = ""
	directory_from = ""
	flash_drive_name = ""

	settings = read_settings()

	if login_credentials == settings[0]: #kijkt of de gegevens van de admin overeenkomen om in te loggen
		print("login good")
		type_of_copy = input("What type of copy?(F = file & D = directory: " )
		if type_of_copy == "F":
			directory_from = input("The directory/Filenaam and extension?" )
		elif type_of_copy == "D":
			directory_from = input("The directory?" )

		if type_of_copy == "F" or type_of_copy == "D":
			flash_drive_name = input("The name of the flash drive: ")

			settings_lijst.append(login_credentials)
			settings_lijst.append(type_of_copy + "\n")
			settings_lijst.append(directory_from + "\n")
			settings_lijst.append(flash_drive_name + "\n")

			write_to_settings = open('settings.txt', 'w')
			for setting in settings_lijst:
				write_to_settings.write(setting)
			write_to_settings.close()
			print(settings_lijst)
	else:
		print("login failed.")
# einde update_settings def

def copy():
	settings = read_settings()
	user = getpass.getuser()
	type_of_copy = settings[1].strip()
	directory_from = "C:/Users/" + user + settings[2].strip()
	directory_to = "F:/"

	if type_of_copy == "F":
		shutil.copy2(directory_from, directory_to)
		print("done")
	elif type_of_copy == "D":
		shutil.copytree(directory_from, directory_to)
		print("done")
# einde copy function

copy()