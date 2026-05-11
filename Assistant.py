import speech_recognition as sr
import webbrowser 
import pyttsx3
from datetime import datetime
import os
import website_list
import app_list
import wikipedia
import logging
import tkinter as tk
import threading
import commands_list




class Underscore():
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.window = tk.Tk()
        self.window.title("Underscore :)")
        self.window.geometry("400x450")
        self.running = False
        self.speech_lock = threading.Lock()
        logging.basicConfig(
                    filename="assistant.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s"
                )
        self.set_gui()
    def set_gui(self):
        self.log_box = tk.Text(self.window, height=20, width= 30, state="disabled")
        self.log_box.pack()
        self.status_label = tk.Label(self.window, text="status: Idle" , fg="gray")
        self.status_label.pack()
        label = tk.Label(self.window, text="Click start to Initialize Underscore")
        start_button = tk.Button(self.window, text="START", command=self.start_assistant)
        stop_button = tk.Button(self.window, text="STOP", command=self.stop_assistant)
        label.pack()
        start_button.pack()
        stop_button.pack()

    def log(self,txt):
        self.window.after(0, lambda: self._log(txt))

    def _log(self,txt):
        self.log_box.config(state="normal")
        self.log_box.insert(tk.END, txt + "\n")
        self.log_box.see(tk.END)
        self.log_box.config(state="disabled")

    def start_assistant(self):
        if self.running:
            return
        self.running = True
        thread = threading.Thread(target=self.assistant,daemon=True)
        thread.start()

    def stop_assistant(self):
        self.running = False
        self.set_status("deactivating Underscore...","black")
        logging.info("deactivating Underscore...")
        self.speak("deactivating underscore...")
        self.set_status("Idle", "gray")

    def set_status(self,txt, color ="black"):
        self.window.after(0, lambda:self.status_label.config(text=f"status: {txt}", fg=color))

    
    
    def speak(self, text):
        with self.speech_lock:
            engine = pyttsx3.init()  
            engine.say(text)
            engine.runAndWait() 
    
    def extract_search_query(self,command , word):
        i = command.find(word)
        o = len(word)+1
        return command[i + o:].strip()

    def process_command(self,c):
        self.set_status("loading...","green")
        logging.info("loading...")
        if("open" in c):
            l = c.split(' ')
            index = l.index("open")+1
            if index < len(l):
                word = l[index]
            else:
                self.log("plz tell me what to open")
                logging.warning("plz tell me what to open")
                self.speak("plz tell me what to open")
                self.set_status("Idle", "gray")
                return
            logging.info(word)
            if(word in website_list.websites):
                link = website_list.websites[word]
                webbrowser.open(link)
                self.set_status("Idle", "gray")
                return
            elif(word in app_list.apps):
                app = app_list.apps[word]
                os.startfile(app)
                self.set_status("Idle", "gray")
                return
            else:
                self.log(f"sorry i dont know how to open {word}")
                logging.warning(f"sorry i dont know how to open {word}")
                self.speak(f"sorry i dont know how to open {word}")
                self.set_status("Idle", "gray")
                return
        for trigger, func in commands_list.commands.items():
            if trigger in c:
                print("Matched:", trigger)
                result = func(c)

                if result:
                    self.log(result)
                    logging.info(result)
                    self.speak(result)

                self.set_status("Idle", "gray")
                return
            
        self.log("Unknown command")
        logging.error("Unknown command")
        self.speak("Sorry, I did not understand that command")
        
    def assistant(self):
        self.set_status("Initializing underscore...", "black")
        logging.info("Initializing underscore...")
        self.speak("Initializing _...")
        while self.running:
            self.set_status("recognizing...", "green")
            logging.info("recognizing...")
            try:
                with sr.Microphone() as source:
                    self.set_status("listening...","green")
                    logging.info("listening...")
                    audio = self.recognizer.listen(source,timeout=2,phrase_time_limit=3)
                command = self.recognizer.recognize_google(audio).lower()
                logging.info(command)
                if("stop" in command):
                    self.stop_assistant()
                    break
                elif("underscore" in command and self.running):
                    self.log("hello sir, how may i help you ?")
                    self.speak("hello sir, how may i help you")
                    with sr.Microphone() as source:
                        self.set_status("listening...", "green")
                        logging.info("listening...")
                        audio = self.recognizer.listen(source,timeout=2, phrase_time_limit=10)
                    command = self.recognizer.recognize_google(audio).lower()
                    print(command)
                    self.log(command)
                    logging.info(command)
                    self.process_command(command)
            except Exception as e:
                logging.error(f"Error: {e}")
                print(f"Error: {e}")

    def run(self):
        self.window.mainloop()


assistant = Underscore()
assistant.run()