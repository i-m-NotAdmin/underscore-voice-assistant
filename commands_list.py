import webbrowser
import wikipedia
import pyjokes
from datetime import datetime

def extract_search_query(command , word):
    i = command.find(word)
    o = len(word)+1
    return command[i + o:].strip()

def google_search(c):
    search = extract_search_query(c,"what")
    webbrowser.open(f"https://www.google.com/search?q=what+{search.replace(' ', '+')}")
    return f"search google for {search}"

def date_time(c):
    current = datetime.now()
    return f"today is {current.strftime('%d %m %y')} and the time is {current.strftime('%I %M %p')}"

def on_wikipedia(c):
    question = extract_search_query(c, "tell me")
    result = wikipedia.summary(f"{question}", sentences= 4)
    return result

def joke(c):
    result = pyjokes.get_joke()
    print("JOKE:", result)
    return result

def sum(c):
    sum = extract_search_query(c,"sum of")
    l = sum.split(" ")
    num1 = int(l[0])
    num2 = int(l[2])
    return num1 + num2

def thanks(c):
    return "I'm glad I could be of help"

commands = {
    "what" : google_search,
    "date and time" : date_time,
    "tell me" : on_wikipedia,
    "make me laugh": joke,
    "sum of" : sum,
    "thankyou" : thanks,
    "thanks" : thanks,
    "thank you" : thanks
}

