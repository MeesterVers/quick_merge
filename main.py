import shutil
import os
import getpass
import ctypes
import datetime
import string

def read_settings():
	settings_list = []
	read_settings_file = open('settings.txt', 'r')
	settings_list = read_settings_file.readlines()
	read_settings_file.close()
	return settings_list
# einde read_settings def

def update_settings(): #funcite waarmee de admin de huidige informatie kan aanpassen
	settings_list = []
	username = input("Username: ")
	password = input("password: ")
	login_credentials = username + ";" + password + "\n"
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

			settings_list.append(login_credentials)
			settings_list.append(type_of_copy + "\n")
			settings_list.append(directory_from + "\n")
			settings_list.append(flash_drive_name + "\n")

			write_to_settings = open('settings.txt', 'w')
			for setting in settings_list:
				write_to_settings.write(setting)
			write_to_settings.close()
			print(settings_list)
	else:
		print("login failed.")
# einde update_settings def

def find_to_flashdrive():
	letters = list(string.ascii_uppercase)
	settings = read_settings()
	name_of_drive = settings[3].strip()

	kernel32 = ctypes.windll.kernel32
	volumeNameBuffer = ctypes.create_unicode_buffer(1024)
	fileSystemNameBuffer = ctypes.create_unicode_buffer(1024)
	serial_number = None
	max_component_length = None
	file_system_flags = None

	for letter in letters:
		rc = kernel32.GetVolumeInformationW(
		    ctypes.c_wchar_p(letter + ':/'),
		    volumeNameBuffer,
		    ctypes.sizeof(volumeNameBuffer),
		    serial_number,
		    max_component_length,
		    file_system_flags,
		    fileSystemNameBuffer,
		    ctypes.sizeof(fileSystemNameBuffer)
		)
		if volumeNameBuffer.value == name_of_drive:
			drive_letter = letter + ":/"
			break
	return drive_letter
#einde find_to_flashdrive def

def copy():
	settings = read_settings()
	user = getpass.getuser()
	type_of_copy = settings[1].strip()
	directory_from = "C:/Users/" + user + settings[2].strip()

	today = datetime.datetime.today()
	today = today.strftime("%d_%b_%y_%H%M%S")
	# directory_to = "C:/Users/" + user + "/Documents/copy"
	directory_to = find_to_flashdrive() + "copy_"+ today

	if type_of_copy == "F":
		shutil.copy2(directory_from, directory_to)
		print("done")
	elif type_of_copy == "D":
		shutil.copytree(directory_from, directory_to)
		print("done")
# einde copy function
copy()