import requests
import os
import tarfile

def main(selection,models):
	tg = '''
 ▄▄▄▄         ██░ ██      ▒███████▒     ▄▄▄█████▓      ██ ▄█▀
▓█████▄      ▓██░ ██▒     ▒ ▒ ▒ ▄▀░     ▓  ██▒ ▓▒      ██▄█▒ 
▒██▒ ▄██     ▒██▀▀██░     ░ ▒ ▄▀▒░      ▒ ▓██░ ▒░     ▓███▄░ 
▒██░█▀       ░▓█ ░██        ▄▀▒   ░     ░ ▓██▓ ░      ▓██ █▄ 
░▓█  ▀█▓ ██▓ ░▓█▒░██▓ ██▓ ▒███████▒ ██▓   ▒██▒ ░  ██▓ ▒██▒ █▄
░▒▓███▀▒ ▒▓▒  ▒ ░░▒░▒ ▒▓▒ ░▒▒ ▓░▒░▒ ▒▓▒   ▒ ░░    ▒▓▒ ▒ ▒▒ ▓▒
▒░▒   ░  ░▒   ▒ ░▒░ ░ ░▒  ░░▒ ▒ ░ ▒ ░▒      ░     ░▒  ░ ░▒ ▒░
 ░    ░  ░    ░  ░░ ░ ░   ░ ░ ░ ░ ░ ░     ░       ░   ░ ░░ ░ 
 ░        ░   ░  ░  ░  ░    ░ ░      ░             ░  ░  ░   
      ░   ░            ░  ░          ░             ░        
        BHZEYE TOOL-KIT: bhzspleeter package wizard'''
	os.system("cls")
	print(tg)
	print(f'''
____________________________________________________________________
2stems = 1 |  2stems-finetuned = 4 |  2,4,5 stems pack = 7          
4stems = 2 |  4stems-finetuned = 5 |  2,4,5 stems-finetuned pack = 8
5stems = 3 |  5stems-finetuned = 6 |  DOWNLOAD FILES ===> 0	
                                                                    
clear selection = "clear" or "c"
check for installed models = "models" or "m"							        
____________________________________________________________________
Current selection: {models}											
____________________________________________________________________

''')
	input_info = input("SELECT--> ")
	if input_info.isdigit():
		already_exists = False
		for i in selection:
			if input_info == i:
				main(selection,models)
		if already_exists == False:
			if input_info == "1":
				selection.append(int(input_info))
				models.append("2stems")
				main(selection,models)
			elif input_info == "2":
				selection.append(int(input_info))
				models.append("4stems")
				main(selection,models)
			elif input_info == "3":
				selection.append(int(input_info))
				models.append("5stems")
				main(selection,models)
			elif input_info == "4":
				selection.append(int(input_info))
				models.append("2stems-finetune")
				main(selection,models)
			elif input_info == "5":
				selection.append(int(input_info))
				models.append("4stems-finetune")
				main(selection,models)
			elif input_info == "6":
				selection.append(int(input_info))
				models.append("5stems-finetune")
				main(selection,models)
			elif input_info == "7":
				selection.append(int(input_info))
				models.append("2,4,5 stems pack")
				main(selection,models)
			elif input_info == "8":
				selection.append(int(input_info))
				models.append("2,4,5 stems-finetuned pack")
				main(selection,models)
			elif input_info == "0":
				download_models(selection)
			else:
				main(selection,models)
		else:
			main(selection,models)
	elif input_info.lower() == "clear":
		main([],[])
	elif input_info.lower() == "c":
		main([],[])
	elif input_info.lower() == "models":
		try:
			print(f'models: {os.listdir(f"{os.getcwd()}/pretrained_models")}')
			input("PRESS ENTER TO CONTINUE")
			main(selection,models)
		except:
			print("could not find 'pretrained_models' directory. . .")
			input("PRESS ENTER TO CONTINUE")
			main(selection,models)
	elif input_info.lower() == "m":
		try:
			print(os.listdir(f"{os.getcwd()}/pretrained_models"))
			input("PRESS ENTER TO CONTINUE")
			main(selection,models)
		except:
			print("could not find 'pretrained_models' directory. . .")
			input("PRESS ENTER TO CONTINUE")
			main(selection,models)
	else:
		a = input("quit:(y/n)")
		if a.upper() == "Y":
			exit()
		else:
			main(selection,models)

def download_models(selec):
	os.system("cls")
	print('''
 ▄▄▄▄         ██░ ██      ▒███████▒     ▄▄▄█████▓      ██ ▄█▀
▓█████▄      ▓██░ ██▒     ▒ ▒ ▒ ▄▀░     ▓  ██▒ ▓▒      ██▄█▒ 
▒██▒ ▄██     ▒██▀▀██░     ░ ▒ ▄▀▒░      ▒ ▓██░ ▒░     ▓███▄░ 
▒██░█▀       ░▓█ ░██        ▄▀▒   ░     ░ ▓██▓ ░      ▓██ █▄ 
░▓█  ▀█▓ ██▓ ░▓█▒░██▓ ██▓ ▒███████▒ ██▓   ▒██▒ ░  ██▓ ▒██▒ █▄
░▒▓███▀▒ ▒▓▒  ▒ ░░▒░▒ ▒▓▒ ░▒▒ ▓░▒░▒ ▒▓▒   ▒ ░░    ▒▓▒ ▒ ▒▒ ▓▒
▒░▒   ░  ░▒   ▒ ░▒░ ░ ░▒  ░░▒ ▒ ░ ▒ ░▒      ░     ░▒  ░ ░▒ ▒░
 ░    ░  ░    ░  ░░ ░ ░   ░ ░ ░ ░ ░ ░     ░       ░   ░ ░░ ░ 
 ░        ░   ░  ░  ░  ░    ░ ░      ░             ░  ░  ░   
      ░   ░            ░  ░          ░             ░        
    BHZEYE TOOL-KIT: bhzspleeter pretrained_models wizard
____________________________________________________________________
	''')

	link_list = ["1","https://github.com/deezer/spleeter/releases/download/v1.4.0/2stems.tar.gz",
				 "https://github.com/deezer/spleeter/releases/download/v1.4.0/4stems.tar.gz",
				 "https://github.com/deezer/spleeter/releases/download/v1.4.0/5stems.tar.gz",
				 "https://github.com/deezer/spleeter/releases/download/v1.4.0/2stems-finetune.tar.gz",
				 "https://github.com/deezer/spleeter/releases/download/v1.4.0/4stems-finetune.tar.gz",
				 "https://github.com/deezer/spleeter/releases/download/v1.4.0/5stems-finetune.tar.gz"]

	for i in selec:
		if i == 7:
			selec = [1,2,3]
			break
		elif i == 8:
			selec = [4,5,6]
			break
		else:
			pass

	try:
		os.mkdir(f"{os.getcwd()}/downloads")
	except:
		pass
	try:
		os.mkdir(f"{os.getcwd()}/pretrained_models")
	except:
		pass


	for i in selec:
		try:
			response = requests.get(f"{link_list[i]}", stream=True)
			total_length = response.headers.get('content-length')
			print(f"selected_file: {link_list[i]}\nsize: {int(total_length)/1000000}mb\nid: {i}")
		except:
			print(f"Could not create connectiom to:\n{link_list[i]}.\n check your internet and permissions. . .")
			input("PRESS ENTER TO CONTINUE")
			main([],[])
	print("____________________________________________________________________")



	for i in selec:
		try:
			file_name = f'{os.getcwd()}/downloads/{link_list[i].rsplit("/", 8)[len(link_list[i].rsplit("/", 8))-1].rsplit(".", 3)[0]}.tar.gz'
			with open(file_name, "wb+") as f:
				response = requests.get(f"{link_list[i]}", stream=True)
				total_length = response.headers.get('content-length')
				if total_length is None: # no content length header
					f.write(response.content)
				else:
					dl = 0
					total_length = int(total_length)
					for data in response.iter_content(chunk_size=4096):
						dl += len(data)
						f.write(data)
						done = int(50 * dl / total_length)
						print("\rDownloading;id=%s.[%s%s]" % (i,'*' * done, ' ' * (50-done)),end="\r")
					try:
						file = tarfile.open(f'{file_name}')
						print("")
						file.extractall(f'{os.getcwd()}/pretrained_models/{link_list[i].rsplit("/", 8)[len(link_list[i].rsplit("/", 8))-1].rsplit(".", 3)[0]}')
					except:
						pass
		except:
			print("Fatal error, could not run program.\n verify permission to read/write (try running as admin),\ncheck permissions for internet,\n check for internet conection")
			a = input("quit:(y/n)")
			if a.upper() == "Y":
				exit()
			else:
				main([],[])
	print("Done downloading models...")
	input("PRESS ENTER TO CONTINUE")
	main([],[])
if __name__ == "__main__":
	if os.path.isfile(f"{os.getcwd()}/bhzspleeter.exe")  == True:
		main([],[])
	else:
		if os.path.isfile(f"{os.getcwd()}/bhzspleeter.py") == True:
			main([],[])
		else:
			print("this directory is not a bhzspleeter enviroment, do u want to run the program anyways ?")
			a = input("(y/n) >")
			if a.upper() == "Y":
				main([],[])
			else:
				exit()