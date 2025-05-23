import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import cv2
import pyautogui
import pygetwindow as gw
import time
import psutil
import pyjokes
import screen_brightness_control as sbc

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am David sir. Say 'start listening' when you need me.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception:
        print("Say that again please...")
        return "None"
    return query

def activeMode():
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("https://youtube.com")

        elif 'open google' in query:
            webbrowser.open("https://www.google.com")

        elif 'open chrome' in query:
            webbrowser.open("https://www.google.com/chrome/")

        elif 'open spotify' in query:
            webbrowser.open("https://spotify.com")

        elif 'play music' in query or 'open music' in query:
            speak("Playing music from your songs folder.")
            music_dir = 'D:\\songs'
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
            else:
                speak("No songs found in the directory.")

        elif 'open notepad' in query:
            speak("Opening Notepad")
            os.system("notepad")

        elif 'open calculator' in query:
            speak("Opening Calculator")
            os.system("calc")

        elif 'open command prompt' in query or 'open cmd' in query:
            speak("Opening Command Prompt")
            os.system("start cmd")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open camera' in query or 'the camera' in query:
            cap = cv2.VideoCapture(0)
            speak("Opening camera. Press Q to exit.")
            while True:
                ret, frame = cap.read()
                cv2.imshow('Camera', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()

        elif 'take a note' in query or 'note this' in query:
            speak("What should I write, sir?")
            note = takeCommand()
            with open("DavidNotes.txt", "a") as f:
                f.write(f"{datetime.datetime.now()}: {note}\n")
            speak("Note saved.")

        elif 'show my notes' in query or 'open my notes' in query:
            speak("Opening your notes")
            os.startfile("DavidNotes.txt")

        elif 'search on google' in query or 'google' in query:
            if 'search' in query and 'on google' in query:
                search_query = query.replace("search", "").replace("on google", "").strip()
            else:
                speak("What should I search on Google?")
                search_query = takeCommand().lower()
            url = f"https://www.google.com/search?q={search_query}"
            speak(f"Searching for {search_query} on Google")
            webbrowser.open(url)

        elif 'close browser' in query:
            speak("Closing Chrome browser")
            os.system("taskkill /im chrome.exe /f")

        elif 'close tab' in query:
            speak("Closing current tab")
            pyautogui.hotkey('ctrl', 'w')

        elif 'close music' in query:
            speak("Closing music player")
            os.system("taskkill /im wmplayer.exe /f")
            os.system("taskkill /im vlc.exe /f")
            os.system("taskkill /im spotify.exe /f")

        elif 'close notepad' in query:
            speak("Closing Notepad")
            os.system("taskkill /im notepad.exe /f")

        elif 'close calculator' in query:
            speak("Closing Calculator")
            os.system("taskkill /im calc.exe /f")

        elif 'close command prompt' in query or 'close cmd' in query:
            speak("Closing Command Prompt")
            os.system("taskkill /im cmd.exe /f")

        elif 'close spotify' in query:
            speak("Closing Spotify")
            os.system("taskkill /im spotify.exe /f")

        elif 'close everything' in query:
            speak("Closing all applications")
            os.system("taskkill /im chrome.exe /f")
            os.system("taskkill /im msedge.exe /f")
            os.system("taskkill /im firefox.exe /f")
            os.system("taskkill /im wmplayer.exe /f")
            os.system("taskkill /im vlc.exe /f")
            os.system("taskkill /im spotify.exe /f")
            os.system("taskkill /im notepad.exe /f")
            os.system("taskkill /im cmd.exe /f")
            os.system("taskkill /im calc.exe /f")

        elif 'increase volume' in query or 'volume up' in query:
            speak("Increasing volume")
            for _ in range(5):
                pyautogui.press("volumeup")

        elif 'decrease volume' in query or 'volume down' in query:
            speak("Decreasing volume")
            for _ in range(5):
                pyautogui.press("volumedown")

        elif 'mute volume' in query or 'mute sound' in query:
            speak("Muting volume")
            pyautogui.press("volumemute")

        elif 'unmute volume' in query or 'unmute sound' in query:
            speak("Unmuting volume")
            pyautogui.press("volumemute")

        elif 'set volume to' in query:
            try:
                level = int([word for word in query.split() if word.isdigit()][0])
                if 0 <= level <= 100:
                    speak(f"Setting volume to {level} percent")
                    for _ in range(50):
                        pyautogui.press("volumedown")
                    for _ in range(level // 2):
                        pyautogui.press("volumeup")
                else:
                    speak("Please provide a number between 0 and 100")
            except:
                speak("Sorry, I couldn't understand the volume level.")

        elif 'increase brightness' in query:
            try:
                current = sbc.get_brightness(display=0)[0]
                new_brightness = min(current + 20, 100)
                sbc.set_brightness(new_brightness)
                speak(f"Increasing brightness to {new_brightness} percent")
            except:
                speak("Failed to change brightness")

        elif 'decrease brightness' in query:
            try:
                current = sbc.get_brightness(display=0)[0]
                new_brightness = max(current - 20, 0)
                sbc.set_brightness(new_brightness)
                speak(f"Decreasing brightness to {new_brightness} percent")
            except:
                speak("Failed to change brightness")

        elif 'set brightness' in query:
            try:
                level = int([word for word in query.split() if word.isdigit()][0])
                if 0 <= level <= 100:
                    sbc.set_brightness(level)
                    speak(f"Setting brightness to {level} percent")
                else:
                    speak("Please provide a number between 0 and 100")
            except:
                speak("Sorry, I couldn't understand the brightness level.")

        elif 'check brightness' in query or 'brightness level' in query:
            try:
                level = sbc.get_brightness(display=0)[0]
                speak(f"The current brightness level is {level} percent")
            except:
                speak("Unable to retrieve brightness level")

        elif 'battery status' in query or 'check battery' in query:
            battery = psutil.sensors_battery()
            percent = battery.percent
            plugged = "charging" if battery.power_plugged else "not charging"
            speak(f"Battery is at {percent} percent and is currently {plugged}")

        elif 'open file manager' in query or 'open explorer' in query:
            speak("Opening File Manager")
            os.system("explorer")

        elif 'close file manager' in query or 'close explorer' in query:
            speak("Closing File Manager")
            os.system("taskkill /f /im explorer.exe")
            time.sleep(1)
            os.system("start explorer.exe")

        elif 'lock screen' in query or 'lock the screen' in query:
            speak("Locking the screen")
            os.system("rundll32.exe user32.dll,LockWorkStation")

        elif 'restart system' in query or 'restart the computer' in query:
            speak("Restarting the system")
            os.system("shutdown /r /t 1")

        elif 'shutdown system' in query or 'shut down the computer' in query:
            speak("Shutting down the system")
            os.system("shutdown /s /t 1")

        elif 'stop listening' in query or 'go to sleep' in query:
            speak("Going to sleep. Say 'start listening' when you need me.")
            break

        elif 'tell me a joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif 'exit' in query or 'quit' in query:
            speak("Okay sir, shutting down. Have a great day!")
            exit()

if __name__ == "__main__":
    wishMe()
    while True:
        print("Waiting for 'start listening'...")
        query = takeCommand().lower()
        if 'start listening' in query:
            speak("I am listening now.")
            activeMode()
