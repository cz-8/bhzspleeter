# bhzspleeter
ui for spleeter

This is a simple ui for spleeter by deezer.

in the source folder u will find the source code for the .py files used to create the ui and separate the audio;
also theres gonna be all the necesary files for u to create a vitrtualenv and run the source python file

and a folder with complementary content that needs to be pasted to the final pyinstaller output folder, otherwise the .exe doesnt run.

finally there will be built .exe zip folders for u to just download and run the program.

in the future i will be adding a .exe that install fine tuned stems on ur bhzspleeter folder;
and a less bloated ui for u to modify more easily.

socials:
cz8   @   https://www.instagram.com/arthurfabris_/
asafe @   https://www.instagram.com/asafecarinss/

contact: bhzeye@tutanota.com (or u can dm on insta)


later i will add the sha256 signature of the built .zip folder and source files.
last_updated @ 22/06/2023 by: cz8

__________________________________________________________________________________

aboutinfo.txt

Author: cz8
Music: asafe
---------------------------------
UI Config parameters:

"dark_theme" expects a boolean ("True" or "False"); example: dark_theme=False

"play_music_on_startup" expects a boolean ("True" or "False"); example: play_music_on_startup=True

"STEM_COUNT" expects either (2 or 4 or 5); example:STEM_COUNT=2

"BITRATE" expects either (128,192,320 or an custom bitrate in the form of an interger; example: BITRATE=320 # k bit/s

"ENCODING" expects [wav|mp3|ogg|m4a|wma|flac] as an input; example: ENCODING=flac
---------------------------------
		
UI Default config:

dark_theme=True
play_music_on_startup=True
STEM_COUNT=2
BITRATE=320
ENCODING=mp3

---------------------------------

Change default UI config:
		
to change the default config u will have to open "ui_config.cfg" in a text editor and edit the settings there
---------------------------------
	
link{1} = https://github.com/deezer/spleeter


last_update @ 22/06/2023

install dependencies:
install.txt
put ffmpeg_bin into the "path" ambient variables

Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/


installvisualc++.png
![install visualc++](https://github.com/cz-8/bhzspleeter/assets/137376594/379e2616-94ea-46b3-944b-d738a5399c9d)
select these options



