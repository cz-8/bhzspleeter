import threading
import pyaudio
import wave
from tkinter import *
import os
import re
from PIL import ImageTk, Image
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
import time
from multiprocessing import freeze_support
from tkinter import messagebox
import os
from datetime import datetime
from dateutil import tz
import bhzSPLEET

RESIZABLE = False
WIDTH, HEIGHT = 640, 480
PATH0 = os.getcwd()
config_list = []

with open("ui_config.cfg","r") as config_file:
	raw_data = config_file.readlines()
	# theme, play_music, stem, bitrate, encoding
	for data in raw_data:
		clean_data = data.strip('\n')
		value = clean_data[clean_data.find('=')+1:]
		config_list.append(value.upper())


if config_list[0] == "TRUE":
	dark_theme = True
elif config_list[0] == "FALSE":
	dark_theme = False
else:
	dark_theme = True

if config_list[1] == "TRUE":
	LET_MUSIC_PLAY = True
elif config_list[1] == "FALSE":
	LET_MUSIC_PLAY = False
else:
	LET_MUSIC_PLAY = True

DEFAULT_STEM_COUNT = int(config_list[2])

DEFAULT_BITRATE = str(config_list[3])

DEFAULT_ENCODING = str(config_list[4])

if dark_theme == True: #dark theme hex values
	FG = "#ffffff"
	BG = "#000000"
	disabled_entry_BG = "#252525"
elif dark_theme == False: #light theme hex value
	FG = "#000000"
	BG = "#ffffff"
	disabled_entry_BG = "#E0E0E0"

if DEFAULT_BITRATE != str(128):
	if DEFAULT_BITRATE != str(192):
		if DEFAULT_BITRATE != str(320):
			custom_bit_rate = DEFAULT_BITRATE

			DEFAULT_BITRATE = -1337


class background_music:

    def __init__(self, master):

        self.song_name = [f for f in os.listdir('background_music') if re.match(r'.*\.wav', f)]

        self.file = f"background_music/{self.song_name[0]}"
        frame = LabelFrame(master,text="Background-music",fg=FG,bg=BG)
        frame.place(x=455,y=10)

        self.pause_btn = Button(master=frame, text="■",borderwidth=0, command=self.pause,fg=FG,bg=BG)
        self.pause_btn.grid(row=0,column=0,sticky=E)

        self.spacer_label = Label(master=frame,text=f"Track:\n{str(self.song_name[0])}",font=("Arial", 7),fg=FG,bg=BG)
        self.spacer_label.grid(row=0,column=2,sticky=E)

        self.play_btn = Button(master=frame, text="▶",borderwidth=0, command=self.play,fg=FG,bg=BG)
        self.play_btn.grid(row=0,column=1,sticky=W)

        

        self.paused = True
        self.playing = False

        self.audio_length = 0
        self.current_sec = 0

    def start_playing(self):  
        
        p = pyaudio.PyAudio()
        chunk = 256
        with wave.open(self.file, "rb") as wf:
            
            self.audio_length = wf.getnframes() / float(wf.getframerate())

            stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

            data = wf.readframes(chunk)

            chunk_total = 0
            while data != b"" and self.playing:

                if not self.paused:
                    chunk_total += chunk
                    stream.write(data)
                    data = wf.readframes(chunk)
                    #self.current_sec = chunk_total/wf.getframerate()

        self.playing=False
        stream.close()   
        p.terminate()

    def pause(self):
        self.playing = False

    
    def play(self):
        
        if not self.playing:
            self.playing = True
            threading.Thread(target=self.start_playing, daemon=True).start()
        self.paused = False

def update_radio_button(identification, *args):

	if identification == "stem_count":
		value = str(stem_count.get())
	elif identification == "bitrate":
		value = str(bitrate.get())
		if value == "-1337":
			for i in args:
				i.config(state="normal")

		else:
			for i in args:
				i.delete(0, END)
				i.config(state="disabled")

	if identification == "encoding":
		value = str(encoding.get())

def about_window(placer):
	if placer == 1:
		os.system(f"{PATH0}/assets/aboutinfo.txt")
	elif placer == 2:
		os.system(f"{PATH0}/ui_config.cfg")


def file_explorer(placer,config_label):

	global FILE_PATH, OUTPUT_PATH, ADVANCED_CONFIG_PATH

	if placer == 1:

		FILE_PATH = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3; *.wav; *.flac;")]) #IMPORTANT_VAR

		if FILE_PATH != "":
			config_label.delete(0,END)
			config_label.insert(END,f"{FILE_PATH}") #IMPORTANT_VAR


		return FILE_PATH


	elif placer == 2:

		OUTPUT_PATH = filedialog.askdirectory()

		if OUTPUT_PATH != "":
			config_label.delete(0,END)
			config_label.insert(END,f"{OUTPUT_PATH}")

		return OUTPUT_PATH


	elif placer == 3:

		ADVANCED_CONFIG_PATH = filedialog.askopenfilename(filetypes=[("Config Files", "*.json")])

		if ADVANCED_CONFIG_PATH != "":
			config_label.delete(0,END)
			config_label.insert(END,f"{ADVANCED_CONFIG_PATH}")


		return ADVANCED_CONFIG_PATH


def bhz_vt(root):
	videoplayer = TkinterVideo(master=root,fg=FG,bg=BG)
	videoplayer.load("assets/video.mp4")
	videoplayer.place(x=485,y=375)
	videoplayer.play()

	while True:
		time.sleep(7)
		videoplayer.play()

def message_display(lbl,txt):
	messagebox.showerror(f'{lbl}', f'{txt}')

def logdata(data,debug,display):

	try:
		os.mkdir("logdata")
	except:
		pass

	filename = f"{os.getcwd()}/logdata/log.txt"
	
	if debug == 1:
		with open(filename, 'a+') as filehandle:
			filehandle.write(f"{datetime.now(tz.gettz())}: {data}\n")
			display.insert(END,f"{data}\n")
	elif debug == 2:
		display.insert(END,f"{data}\n")
	else:
		with open(filename, 'a+') as filehandle:
			filehandle.write(f"{datetime.now(tz.gettz())}: {data}\n")


def wait_for_del(a,plc):
	if plc == 0:
		time.sleep(3)
		a.destroy()
	elif plc == 1:
		tag1 = r'''
                    $$\                      $$\     $$\                                       $$\                                                 
                    $$ |                     $$ |    \__|                                      $$ |                                                
 $$$$$$$\  $$$$$$\  $$ | $$$$$$\   $$$$$$\ $$$$$$\   $$\ $$$$$$$\   $$$$$$\         $$$$$$$\ $$$$$$\    $$$$$$\  $$$$$$\$$$$\   $$$$$$$\           
$$  _____|$$  __$$\ $$ |$$  __$$\ $$  __$$\\_$$  _|  $$ |$$  __$$\ $$  __$$\       $$  _____|\_$$  _|  $$  __$$\ $$  _$$  _$$\ $$  _____|          
\$$$$$$\  $$ /  $$ |$$ |$$$$$$$$ |$$$$$$$$ | $$ |    $$ |$$ |  $$ |$$ /  $$ |      \$$$$$$\    $$ |    $$$$$$$$ |$$ / $$ / $$ |\$$$$$$\            
 \____$$\ $$ |  $$ |$$ |$$   ____|$$   ____| $$ |$$\ $$ |$$ |  $$ |$$ |  $$ |       \____$$\   $$ |$$\ $$   ____|$$ | $$ | $$ | \____$$\           
$$$$$$$  |$$$$$$$  |$$ |\$$$$$$$\ \$$$$$$$\  \$$$$  |$$ |$$ |  $$ |\$$$$$$$ |      $$$$$$$  |  \$$$$  |\$$$$$$$\ $$ | $$ | $$ |$$$$$$$  |      $$\ 
\_______/ $$  ____/ \__| \_______| \_______|  \____/ \__|\__|  \__| \____$$ |      \_______/    \____/  \_______|\__| \__| \__|\_______/       \__|
          $$ |                                                     $$\   $$ |                                                                      
          $$ |                                                     \$$$$$$  |                                                                      
          \__|                                                      \______/                                                                       
		'''
		tag2 = r'''
                    $$\                      $$\     $$\                                       $$\                                                           
                    $$ |                     $$ |    \__|                                      $$ |                                                          
 $$$$$$$\  $$$$$$\  $$ | $$$$$$\   $$$$$$\ $$$$$$\   $$\ $$$$$$$\   $$$$$$\         $$$$$$$\ $$$$$$\    $$$$$$\  $$$$$$\$$$$\   $$$$$$$\                     
$$  _____|$$  __$$\ $$ |$$  __$$\ $$  __$$\\_$$  _|  $$ |$$  __$$\ $$  __$$\       $$  _____|\_$$  _|  $$  __$$\ $$  _$$  _$$\ $$  _____|                    
\$$$$$$\  $$ /  $$ |$$ |$$$$$$$$ |$$$$$$$$ | $$ |    $$ |$$ |  $$ |$$ /  $$ |      \$$$$$$\    $$ |    $$$$$$$$ |$$ / $$ / $$ |\$$$$$$\                      
 \____$$\ $$ |  $$ |$$ |$$   ____|$$   ____| $$ |$$\ $$ |$$ |  $$ |$$ |  $$ |       \____$$\   $$ |$$\ $$   ____|$$ | $$ | $$ | \____$$\                     
$$$$$$$  |$$$$$$$  |$$ |\$$$$$$$\ \$$$$$$$\  \$$$$  |$$ |$$ |  $$ |\$$$$$$$ |      $$$$$$$  |  \$$$$  |\$$$$$$$\ $$ | $$ | $$ |$$$$$$$  |      $$\       $$\ 
\_______/ $$  ____/ \__| \_______| \_______|  \____/ \__|\__|  \__| \____$$ |      \_______/    \____/  \_______|\__| \__| \__|\_______/       \__|      \__|
          $$ |                                                     $$\   $$ |                                                                                
          $$ |                                                     \$$$$$$  |                                                                                
          \__|                                                      \______/                                                                                 
		'''
		tag3 = r'''
                    $$\                      $$\     $$\                                       $$\                                                                     
                    $$ |                     $$ |    \__|                                      $$ |                                                                    
 $$$$$$$\  $$$$$$\  $$ | $$$$$$\   $$$$$$\ $$$$$$\   $$\ $$$$$$$\   $$$$$$\         $$$$$$$\ $$$$$$\    $$$$$$\  $$$$$$\$$$$\   $$$$$$$\                               
$$  _____|$$  __$$\ $$ |$$  __$$\ $$  __$$\\_$$  _|  $$ |$$  __$$\ $$  __$$\       $$  _____|\_$$  _|  $$  __$$\ $$  _$$  _$$\ $$  _____|                              
\$$$$$$\  $$ /  $$ |$$ |$$$$$$$$ |$$$$$$$$ | $$ |    $$ |$$ |  $$ |$$ /  $$ |      \$$$$$$\    $$ |    $$$$$$$$ |$$ / $$ / $$ |\$$$$$$\                                
 \____$$\ $$ |  $$ |$$ |$$   ____|$$   ____| $$ |$$\ $$ |$$ |  $$ |$$ |  $$ |       \____$$\   $$ |$$\ $$   ____|$$ | $$ | $$ | \____$$\                               
$$$$$$$  |$$$$$$$  |$$ |\$$$$$$$\ \$$$$$$$\  \$$$$  |$$ |$$ |  $$ |\$$$$$$$ |      $$$$$$$  |  \$$$$  |\$$$$$$$\ $$ | $$ | $$ |$$$$$$$  |      $$\       $$\       $$\ 
\_______/ $$  ____/ \__| \_______| \_______|  \____/ \__|\__|  \__| \____$$ |      \_______/    \____/  \_______|\__| \__| \__|\_______/       \__|      \__|      \__|
          $$ |                                                     $$\   $$ |                                                                                          
          $$ |                                                     \$$$$$$  |                                                                                          
          \__|                                                      \______/                                                                                           
		'''
		os.system("cls")
		while os.path.isfile(f"{os.getcwd()}/finishedtoken1.token") == False:
			os.system("cls")
			print(f"{tag1}",end="")
			time.sleep(0.3)
			os.system("cls")
			print(f"{tag2}",end="")
			time.sleep(0.3)
			os.system("cls")
			print(f"{tag3}",end="")
			time.sleep(0.3)

		os.system("cls")
		tag = r'''
$$\       $$\                                     $$\                      $$\                         
$$ |      $$ |                                    $$ |                     $$ |                        
$$$$$$$\  $$$$$$$\  $$$$$$$$\  $$$$$$$\  $$$$$$\  $$ | $$$$$$\   $$$$$$\ $$$$$$\    $$$$$$\   $$$$$$\  
$$  __$$\ $$  __$$\ \____$$  |$$  _____|$$  __$$\ $$ |$$  __$$\ $$  __$$\\_$$  _|  $$  __$$\ $$  __$$\ 
$$ |  $$ |$$ |  $$ |  $$$$ _/ \$$$$$$\  $$ /  $$ |$$ |$$$$$$$$ |$$$$$$$$ | $$ |    $$$$$$$$ |$$ |  \__|
$$ |  $$ |$$ |  $$ | $$  _/    \____$$\ $$ |  $$ |$$ |$$   ____|$$   ____| $$ |$$\ $$   ____|$$ |      
$$$$$$$  |$$ |  $$ |$$$$$$$$\ $$$$$$$  |$$$$$$$  |$$ |\$$$$$$$\ \$$$$$$$\  \$$$$  |\$$$$$$$\ $$ |      
\_______/ \__|  \__|\________|\_______/ $$  ____/ \__| \_______| \_______|  \____/  \_______|\__|      
                                        $$ |                                                           
                                        $$ |                                                           
                                        \__|                                                           
			'''
		print(f"{tag}",end="")
		file,location = 'finishedtoken1.token',f"{os.getcwd()}"
		path = os.path.join(location, file)  
		os.remove(path)

def compile_config(stem_count,bitrate,encoding,FILE_PATH,OUTPUT_PATH,ADVANCED_CONFIG_PATH,program_state_display,config_choice,custom_bitrate_entry,root):
	os.system("cls")
	tag = r'''
$$\       $$\                                     $$\                      $$\                         
$$ |      $$ |                                    $$ |                     $$ |                        
$$$$$$$\  $$$$$$$\  $$$$$$$$\  $$$$$$$\  $$$$$$\  $$ | $$$$$$\   $$$$$$\ $$$$$$\    $$$$$$\   $$$$$$\  
$$  __$$\ $$  __$$\ \____$$  |$$  _____|$$  __$$\ $$ |$$  __$$\ $$  __$$\\_$$  _|  $$  __$$\ $$  __$$\ 
$$ |  $$ |$$ |  $$ |  $$$$ _/ \$$$$$$\  $$ /  $$ |$$ |$$$$$$$$ |$$$$$$$$ | $$ |    $$$$$$$$ |$$ |  \__|
$$ |  $$ |$$ |  $$ | $$  _/    \____$$\ $$ |  $$ |$$ |$$   ____|$$   ____| $$ |$$\ $$   ____|$$ |      
$$$$$$$  |$$ |  $$ |$$$$$$$$\ $$$$$$$  |$$$$$$$  |$$ |\$$$$$$$\ \$$$$$$$\  \$$$$  |\$$$$$$$\ $$ |      
\_______/ \__|  \__|\________|\_______/ $$  ____/ \__| \_______| \_______|  \____/  \_______|\__|      
                                        $$ |                                                           
                                        $$ |                                                           
                                        \__|                                                           
			'''
	print(f"{tag}",end="")

	logdata("!!! STARTING SESSION !!!",1,program_state_display)
	error = False
	
	if config_choice == 1:


		if int(stem_count) == 2 or 4 or 5:

			logdata(f"Stem count >>> [{stem_count}]",1,program_state_display)
		else:
			error = True
			logdata(f"Stems form has a invalid input >>> [{stem_count}]",1,program_state_display)
			message_display("INPUT ERROR","Stems form has a invalid input. \n Read the manual on usage. . .")

		if bitrate == -1337:
			if custom_bitrate_entry.isdigit() == True:
				bitrate = int(custom_bitrate_entry)
				logdata(f"Bitrate(custom) >>> [{bitrate}]",1,program_state_display)
			else:
				error = True
				logdata(f"{datetime.now(tz.gettz())}¨¨Bitrate(custom) has a invalid input >>> [{bitrate}]",1,program_state_display)
				message_display("INPUT ERROR","Custom bitrate entry has a invalid input. \n Read the manual on usage. . .")
		elif bitrate == 128:
			logdata(f"Bitrate >>> [{bitrate}]",1,program_state_display)
		elif bitrate == 192:
			logdata(f"Bitrate >>> [{bitrate}]",1,program_state_display)
		elif bitrate == 320:
			logdata(f"Bitrate >>> [{bitrate}]",1,program_state_display)
		else:
			error = True
			logdata(f"Bitrate has a invalid input >>> [{bitrate}]",1,program_state_display)
			message_display("INPUT ERROR","BITRATE FORM has a invalid input.\n Read the manual on usage. . .")

		acepted_enc_list = ["wav","mp3","ogg","m4a","wma","flac"]

		encoding_clean = str(encoding).lower()

		j = 0

		for enc in acepted_enc_list:
			if encoding_clean == enc:
				j += 1
			else:
				pass
		if j >= 1:
			logdata(f"Encoding >>> [{encoding}]",1,program_state_display)
		else:
			error = True
			logdata(f"Encoding has a invalid input >>> [{encoding}]",1,program_state_display)
			message_display("INPUT ERROR","ENCODING FORM has a invalid input. \n acepted_encoding_list = '[wav,mp3,ogg,m4a,wma,flac] \n Read the manual on usage. . .")
			

		if os.path.isfile(FILE_PATH) == True:
			if re.match(r'.*\.wav', FILE_PATH):
				logdata(f"Audio file is OK!! type >>> [wav];path: {FILE_PATH}",1,program_state_display)
			elif re.match(r'.*\.mp3', FILE_PATH):
				logdata(f"Audio file is OK!! type >>> [mp3];path: {FILE_PATH}",1,program_state_display)
			elif re.match(r'.*\.flac', FILE_PATH):
				logdata(f"Audio file is OK!! type >>> [flac];path: {FILE_PATH}",1,program_state_display)
			else:
				error = True
				logdata("The type of audio file selected is not supported",1,program_state_display)
				message_display("FILETYPE ERROR","The type of file selected is not supported. \n Read the manual on usage. . .")
		else:
			error = True
			logdata("Audio File path is not valid. . .",1,program_state_display)
			message_display("INPUT ERROR","FILEPATH ENTRY has a invalid input. \n Read the manual on usage. . .")

		if os.path.exists(OUTPUT_PATH) == True:
			logdata(f"OUTPUT_PATH >>> [{OUTPUT_PATH}]",1,program_state_display)
		else:
			error = True
			logdata("OUTPUTPATH is not valid. . . ",1,program_state_display)
			message_display("INPUT ERROR","OUTPUTPATH ENTRY has a invalid input. \n Read the manual on usage. . .")

		if error == False:
			logdata("STARTING TO SPLEET STEMS. . . ",1,program_state_display)
			threading.Thread(target=bhzSPLEET.spleet_stems,args = (1,stem_count,bitrate,encoding.lower(),FILE_PATH,OUTPUT_PATH),daemon = True).start()
			root.update()
			spleeting_label = Label(root,text="",fg=FG,bg=BG)
			spleeting_label.place(x=0,y=355)
			threading.Thread(target=wait_for_del, args=([spleeting_label,1]),daemon = True).start()
			step = 1/3
			while os.path.isfile(f"{os.getcwd()}/finishedtoken.token") == False:
				spleeting_label.config(text="Spleeting stems [.]")
				root.update()
				time.sleep(step)
				spleeting_label.config(text=r"Spleeting stems [. .]")
				root.update()
				time.sleep(step)
				spleeting_label.config(text="Spleeting stems [. . .]")
				root.update()
				time.sleep(step)
			spleeting_label.config(text="FINISHED SPLEETING STEMS. . .")
			threading.Thread(target=wait_for_del, args=([spleeting_label,0]),daemon = True).start()
			logdata("Finished spleeting Stems",1,program_state_display)
			file,location = 'finishedtoken.token',f"{os.getcwd()}"
			path = os.path.join(location, file)  
			os.remove(path)
			logdata("SESSION ENDED!!!",1,program_state_display)

	elif config_choice == 0:

		if os.path.isfile(ADVANCED_CONFIG_PATH) == True:
			if re.match(r'.*\.json', ADVANCED_CONFIG_PATH):
				logdata("ADVANCED_CONFIG_PATH is OK!! type >>> [json]",1,program_state_display)
			else:
				error = True
				logdata("ADVANCED_CONFIG_PATH type is not supported. . .",1,program_state_display)
				message_display("FILETYPE ERROR (ADVANCED_CONFIG_PATH)","The type of file selected is not supported. \n Read the manual on usage. . .")
		else:
			error = True
			message_display("INPUT ERROR","ADVANCED_CONFIG_PATH ENTRY has a invalid input. \n Read the manual on usage. . .")

		if os.path.isfile(FILE_PATH) == True:
			if re.match(r'.*\.wav', FILE_PATH):
				logdata("type >>> [wav]",1,program_state_display)
			elif re.match(r'.*\.mp3', FILE_PATH):
				logdata("type >>> [mp3]",1,program_state_display)
			elif re.match(r'.*\.flac', FILE_PATH):
				logdata("type >>> [flac]",1,program_state_display)
			else:
				error = True
				logdata("The type of audio file selected is not supported",1,program_state_display)
				message_display("FILETYPE ERROR","The type of file selected is not supported. \n Read the manual on usage. . .")
		else:
			error = True
			logdata("Audio File path is not valid. . .",1,program_state_display)
			message_display("INPUT ERROR","FILEPATH ENTRY has a invalid input. \n Read the manual on usage. . .")

		if os.path.exists(OUTPUT_PATH) == True:
			logdata(f"OUTPUT_PATH >>> [{OUTPUT_PATH}]",1,program_state_display)
		else:
			error = True
			logdata("OUTPUTPATH is not valid. . . ",1,program_state_display)
			message_display("INPUT ERROR","OUTPUTPATH ENTRY has a invalid input. \n Read the manual on usage. . .")

		if error == False:
			logdata("STARTING TO SPLEET STEMS. . . ",1,program_state_display)
			threading.Thread(target=bhzSPLEET.spleet_stems,args = (0,ADVANCED_CONFIG_PATH,FILE_PATH,OUTPUT_PATH),daemon = True).start()
			root.update()
			spleeting_label = Label(root,text="",fg=FG,bg=BG)
			spleeting_label.place(x=0,y=355)
			threading.Thread(target=wait_for_del, args=([spleeting_label,1]),daemon = True).start()
			step = 1/3
			while os.path.isfile(f"{os.getcwd()}/finishedtoken.token") == False:
				spleeting_label.config(text="Spleeting stems [.]")
				root.update()
				time.sleep(step)
				spleeting_label.config(text=r"Spleeting stems [. .]")
				root.update()
				time.sleep(step)
				spleeting_label.config(text="Spleeting stems [. . .]")
				root.update() 
				time.sleep(step)
			spleeting_label.config(text="FINISHED SPLEETING STEMS. . .")
			threading.Thread(target=wait_for_del, args=([spleeting_label,0]),daemon = True).start()
			logdata("Finished spleeting Stems",1,program_state_display)
			file,location = 'finishedtoken.token',f"{os.getcwd()}"
			path = os.path.join(location, file)  
			os.remove(path)
			logdata("SESSION ENDED!!!",1,program_state_display)
		else:
			logdata(f"{datetime.now(tz.gettz())}¨¨SESSION END. . . ",1,program_state_display)
			message_display("FATAL ERROR","Config is not valid!!!\nPlease try again \nif you think this is an error please get in contact \n Read the manual on usage. . .")




def main_window():

	global stem_count, bitrate, encoding, program_state_display,root

	os.system("cls")
	tag = r'''
$$\       $$\                                     $$\                      $$\                         
$$ |      $$ |                                    $$ |                     $$ |                        
$$$$$$$\  $$$$$$$\  $$$$$$$$\  $$$$$$$\  $$$$$$\  $$ | $$$$$$\   $$$$$$\ $$$$$$\    $$$$$$\   $$$$$$\  
$$  __$$\ $$  __$$\ \____$$  |$$  _____|$$  __$$\ $$ |$$  __$$\ $$  __$$\\_$$  _|  $$  __$$\ $$  __$$\ 
$$ |  $$ |$$ |  $$ |  $$$$ _/ \$$$$$$\  $$ /  $$ |$$ |$$$$$$$$ |$$$$$$$$ | $$ |    $$$$$$$$ |$$ |  \__|
$$ |  $$ |$$ |  $$ | $$  _/    \____$$\ $$ |  $$ |$$ |$$   ____|$$   ____| $$ |$$\ $$   ____|$$ |      
$$$$$$$  |$$ |  $$ |$$$$$$$$\ $$$$$$$  |$$$$$$$  |$$ |\$$$$$$$\ \$$$$$$$\  \$$$$  |\$$$$$$$\ $$ |      
\_______/ \__|  \__|\________|\_______/ $$  ____/ \__| \_______| \_______|  \____/  \_______|\__|      
                                        $$ |                                                           
                                        $$ |                                                           
                                        \__|                                                           
			'''
	print(f"{tag}",end="")



	#window config
	root = Tk()
	root.geometry(f"{WIDTH}x{HEIGHT}")
	root.resizable(RESIZABLE, RESIZABLE)
	try:
		root.iconbitmap(f"{PATH0}/assets/favicon.ico")
	except:
		pass
	root.title("BHZSPLEETER")
	root.config(bg=BG)

	try:
		player = background_music(root)
	except:
		pass
	try:	
		if LET_MUSIC_PLAY:
			player.play()
		else:
			pass
	except:
		pass

	stems_count_frame = LabelFrame(root)

	stem_count = IntVar(stems_count_frame, DEFAULT_STEM_COUNT) #IMPORTANT_VAR

	stems_count_frame.config(text="Stems count",
		padx=12,
		pady=12,
		relief=GROOVE,fg=FG,bg=BG)
	stems_btn_1 = Radiobutton(stems_count_frame,text="2 STEMS  ",
		variable=stem_count,
		value=2,
        command= lambda:update_radio_button("stem_count"),fg=FG,bg=BG,selectcolor=BG)
	stems_btn_2 = Radiobutton(stems_count_frame,text="4 STEMS  ",
		variable=stem_count,
		value=4,
        command= lambda:update_radio_button("stem_count"),fg=FG,bg=BG,selectcolor=BG)
	stems_btn_3 = Radiobutton(stems_count_frame,text="5 STEMS  ",
		variable=stem_count,
		value=5,
        command= lambda:update_radio_button("stem_count"),fg=FG,bg=BG,selectcolor=BG)



	bitrate_frame = LabelFrame(root)
	bitrate_frame.config(text="Bitrate",
		padx=12,
		pady=4,
		relief=GROOVE,
		fg=FG,bg=BG)

	bitrate = IntVar(bitrate_frame, DEFAULT_BITRATE) #IMPORTANT_VAR

	bitrate_btn_1 = Radiobutton(bitrate_frame,text="128K",
		variable=bitrate,
		value=128,
        command= lambda:update_radio_button("bitrate",custom_bitrate_entry),fg=FG,bg=BG,selectcolor=BG)

	bitrate_btn_2 = Radiobutton(bitrate_frame,text="192K",
		variable=bitrate,
		value=192,
        command= lambda:update_radio_button("bitrate",custom_bitrate_entry),fg=FG,bg=BG,selectcolor=BG)

	bitrate_btn_3 = Radiobutton(bitrate_frame,text="320K",
		variable=bitrate,
		value=320,
        command= lambda:update_radio_button("bitrate",custom_bitrate_entry),fg=FG,bg=BG,selectcolor=BG)

	bitrate_btn_4 = Radiobutton(bitrate_frame,text="Custom bitrate",
		variable=bitrate,
		value=-1337,
        command= lambda:update_radio_button("bitrate",custom_bitrate_entry),fg=FG,bg=BG,selectcolor=BG)


	custom_bitrate_frame = LabelFrame(bitrate_frame)

	custom_bitrate_frame.config(text="Custom-Bitrate",
		relief=GROOVE,
		fg=FG,bg=BG)

	custom_bitrate_entry = Entry(custom_bitrate_frame)
	try:
		custom_bitrate_entry.insert(0,custom_bit_rate)
	except:
		pass
	custom_bitrate_entry.config(width=10,fg=FG,bg=BG,disabledbackground=disabled_entry_BG)
	custom_bitrate_lbl = Label(custom_bitrate_frame)
	custom_bitrate_lbl.config(text="K bit/s",fg=FG,bg=BG)

	encoding_frame = LabelFrame(root)

	encoding = StringVar(encoding_frame, DEFAULT_ENCODING) # [wav|mp3|ogg|m4a|wma|flac] #IMPORTANT_VAR

	encoding_frame.config(text="Encoding",
		padx=12,
		pady=12,
		relief=GROOVE,
		fg=FG,bg=BG)
	encoding_button_1 = Radiobutton(encoding_frame,text=".wav",
		variable=encoding,
		value="WAV",
        command= lambda:update_radio_button("encoding"),fg=FG,bg=BG,selectcolor=BG)
	encoding_button_2 = Radiobutton(encoding_frame,text=".mp3",
		variable=encoding,
		value="MP3",
        command= lambda:update_radio_button("encoding"),fg=FG,bg=BG,selectcolor=BG)
	encoding_button_3 = Radiobutton(encoding_frame,text=".ogg",
		variable=encoding,
		value="OGG",
        command= lambda:update_radio_button("encoding"),fg=FG,bg=BG,selectcolor=BG)
	encoding_button_4 = Radiobutton(encoding_frame,text=".m4a",
		variable=encoding,
		value="M4A",
        command= lambda:update_radio_button("encoding"),fg=FG,bg=BG,selectcolor=BG)
	encoding_button_5 = Radiobutton(encoding_frame,text=".wma",
		variable=encoding,
		value="WMA",
        command= lambda:update_radio_button("encoding"),fg=FG,bg=BG,selectcolor=BG)
	encoding_button_6 = Radiobutton(encoding_frame,text=".flac",
		variable=encoding,
		value="FLAC",
        command= lambda:update_radio_button("encoding"),fg=FG,bg=BG,selectcolor=BG)


	about_info_button = Button(root,text="🌐 info",font=("Arial",12),
		height=1, width=6,
		command= lambda:threading.Thread(target=about_window(1), daemon=True).start(),
		fg=FG,bg=BG)

	filepath_frame = LabelFrame(root,text="Select-file",
		padx=12,
		pady=12,
		relief=GROOVE,
		fg=FG,bg=BG)
	filepath_label = Label(filepath_frame,text="🗁PATH:  ",fg=FG,bg=BG)
	filler1 = Label(filepath_frame,text="  ",fg=FG,bg=BG)
	filepath_entry = Entry(filepath_frame)
	filepath_entry.config(width=75,fg=FG,bg=BG,disabledbackground=disabled_entry_BG)


	filepath_button = Button(filepath_frame,text="Browse files",
		fg=FG,bg=BG,
		relief=GROOVE,
		command=lambda:file_explorer(1,filepath_entry))

	output_path_frame = LabelFrame(root,text="Select-output-directory",
		padx=12,
		pady=12,
		relief=GROOVE,
		fg=FG,bg=BG)
	output_path_label = Label(output_path_frame,text="🗁PATH:  ",fg=FG,bg=BG)
	filler2 = Label(output_path_frame,text="  ",fg=FG,bg=BG)
	output_path_entry = Entry(output_path_frame)
	output_path_entry.config(width=75,fg=FG,bg=BG,disabledbackground=disabled_entry_BG)


	output_path_button = Button(output_path_frame,text="Browse dirs",
		fg=FG,bg=BG,
		relief=GROOVE,
		command=lambda:file_explorer(2,output_path_entry))

	advanced_config_frame = LabelFrame(root,text="(ADVANCED)Select-custom-config-file-(.json)",
		padx=12,
		pady=12,
		relief=GROOVE,
		fg=FG,bg=BG)
	advanced_config_label = Label(advanced_config_frame,text="🗁PATH:  ",fg=FG,bg=BG)

	filler3 = Label(advanced_config_frame,text="  ",fg=FG,bg=BG)
	advanced_config_entry = Entry(advanced_config_frame)
	advanced_config_entry.config(width=75,fg=FG,bg=BG,disabledbackground=disabled_entry_BG)


	advanced_config_button = Button(advanced_config_frame,text="Browse files",
		fg=FG,bg=BG,
		relief=GROOVE,
		command=lambda:file_explorer(3,advanced_config_entry))
	

	config_choice = IntVar(root, 1) #IMPORTANT_VAR

	spleet_stems_frame = LabelFrame(root,text="Config-choice",fg=FG,bg=BG,
		padx=4,
		relief=GROOVE,)

	C1 = Checkbutton(spleet_stems_frame, text = "Normal-config", variable = config_choice,onvalue = 1, offvalue = 0,fg=FG,bg=BG,selectcolor=BG)
	C2 = Checkbutton(spleet_stems_frame, text = "(ADVANCED).json-config", variable = config_choice,onvalue = 0, offvalue = 1,fg=FG,bg=BG,selectcolor=BG)

	spleet_button = Button(root,text="START SPLEETING STEMS",fg=FG,bg=BG,
		height=3, width=40,command=lambda:compile_config(stem_count.get(), bitrate.get(), encoding.get(),filepath_entry.get(),output_path_entry.get(),advanced_config_entry.get(),program_state_display,config_choice.get(),custom_bitrate_entry.get(),root))
														# stem_count,bitrate,encoding,FILE_PATH,OUTPUT_PATH,ADVANCED_CONFIG_PATH,program_state_display,config_choice,custom_bitrate_entry,root
	program_state_display = Text(root)
	program_state_display.config(fg=FG,bg=BG,
		width=50,
		height=4,
		font=("System", 10),
		bd=0)


	open_ui_cfg_button = Button(root,text="🌐ui_cfg",font=("Arial",12),
		height=1, width=6,
		command= lambda:threading.Thread(target=about_window(2), daemon=True).start(),
		fg=FG,bg=BG)





	#========================= POSITIONS =========================
	root.columnconfigure(0, weight=1)
	root.columnconfigure(1, weight=2)
	stems_count_frame.place(x=10,y=10)
	stems_btn_1.pack()
	stems_btn_2.pack()
	stems_btn_3.pack()
	bitrate_frame.place(x=120,y=10)
	bitrate_btn_1.grid(row=0,column=0,sticky=W)
	bitrate_btn_2.grid(row=1,column=0,sticky=W)
	bitrate_btn_3.grid(row=2,column=0,sticky=W)
	bitrate_btn_4.grid(row=0,column=1,sticky=W)

	custom_bitrate_frame.grid(row=1,column=1,sticky=E)
	custom_bitrate_entry.grid(row=1,column=0,sticky=W)
	custom_bitrate_lbl.grid(row=1,column=2,sticky=E)
	encoding_frame.place(x=312,y=10)
	encoding_button_1.grid(row=0,column=0,sticky=W)
	encoding_button_2.grid(row=1,column=0,sticky=W)
	encoding_button_3.grid(row=2,column=0,sticky=W)
	encoding_button_4.grid(row=0,column=1,sticky=W)
	encoding_button_5.grid(row=1,column=1,sticky=W)
	encoding_button_6.grid(row=2,column=1,sticky=W)

	about_info_button.place(x=0,y=441)
	open_ui_cfg_button.place(x=0,y=407)

	filepath_frame.place(x=10,y=140)
	filepath_entry.grid(row=0,column=1,sticky=W)
	filepath_label.grid(row=0,column=0,sticky=W)
	filler1.grid(row=0,column=2,sticky=W)
	filepath_button.grid(row=0,column=3,sticky=W)

	output_path_frame.place(x=10,y=210)

	output_path_label.grid(row=0,column=0,sticky=W)
	output_path_entry.grid(row=0,column=1,sticky=W)
	filler2.grid(row=0,column=2,sticky=W)
	output_path_button.grid(row=0,column=3,sticky=W)

	advanced_config_frame.place(x=10,y=280)
	advanced_config_label.grid(row=0,column=0,sticky=W)
	advanced_config_entry.grid(row=0,column=1,sticky=W)
	filler3.grid(row=0,column=2,sticky=W)
	advanced_config_button.grid(row=0,column=3,sticky=W)

	spleet_stems_frame.place(x=455,y=59)
	C1.grid(row=0,column=0,sticky=W)
	C2.grid(row=1,column=0,sticky=W)
	spleet_button.place(x=175,y=355)
	program_state_display.place(x=68,y=412)
	threading.Thread(target=lambda:bhz_vt(root), daemon=True).start()
	root.mainloop()


if __name__ == "__main__":
	freeze_support()
	main_window()

