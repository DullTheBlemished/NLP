"""Basic 4D vector system that mimics the ones used by real AI models, but is too small, such it is only an above basic keyword search.

fuctions: GetReply(input), spellcheck(input), listen(), voice_reply(reply)

extras: explain_logic(), print_credits(), print_feature()

-Hung
"""
import os
import time
import numpy as np
import random as r
from spellchecker import SpellChecker as sc
import ezspell
import sounddevice as sd
import speech_recognition as sr
import pyttsx3 as tts
# ---------Libary initilization(s)---------
checker = sc()
# -----------------------------------------
# the imports below are copied from ai, used for time inquiries
from datetime import datetime
from zoneinfo import ZoneInfo
# end of ai part (i used ai for this bc its a small part and my project is mainly
# focused on the logic and me practising the vector system)

class NoInputDetectedError(Exception): 
    pass

class SeverRequestFailiure(Exception):
    pass

class InputUnrecognisedError(Exception):
    pass

# you can ignore these for whoever is reading, these notes are for meh
# [1,0,0,0]
greeting = [
    "Hello", 
    "Hi, im NOTai, made by Hung and C(redacted for portfolio)",
    "Wassup", 
    "Salutations indeed!"
]

# [0,1,0,0]
insults = [
    "Now i would respond to you with AM's hate speech but you're not worth my time", 
    "Even though im not an ai im still 100 times more superior then you"
]


# [0,0,1,0]
name_inquiry = [
    "I'm NOTai by christain and hung", 
    "I'm NOTai, what about your's?"
]

# [0,0,0,1]
schedule_inquiry = [
    "if you go to (redacted for portfolio), just open google onto your (redacted for portfolio) page, your student id is the username and your password is your student login"
]

weights = { # GREETINGS ([0.3, 0, 0, 0]) - LINEAR WEIGHT
           "hello": np.array([0.3, 0, 0, 0]),
           "hi": np.array([0.3, 0, 0, 0]),
           "greetings": np.array([0.3, 0, 0, 0]),
           "howdy": np.array([0.3, 0, 0, 0]),
           "hullo": np.array([0.3, 0, 0, 0]),
           "salutations": np.array([0.3, 0, 0, 0]),
           "allo": np.array([0.3, 0, 0, 0]),
           "morning": np.array([0.3, 0, 0, 0]),
           "evening": np.array([0.3, 0, 0, 0]),
           "afternoon": np.array([0.3, 0, 0, 0]),
           
           # INSULTS ([0, ?, 0, 0]) - NON-LINEAR WEIGHT
           "bum": np.array([0, 1, 0, 0]),
           "mid": np.array([0, 1, 0, 0]),
           "npc": np.array([0, 1, 0, 0]),
           "stupid": np.array([0, 1.5, 0, 0]),
           "dumb": np.array([0, 1.5, 0, 0]),
           "idiot": np.array([0, 1.5, 0, 0]),
           "useless": np.array([0, 1.5, 0, 0]),
           "incompetent": np.array([0, 1.5, 0, 0]),
           "pathetic": np.array([0, 2.3, 0, 0]),
           "defective": np.array([0, 2.3, 0, 0]),

           # NAME INQUIRY ([0, 0, ?, 0]) - NON-LINEAR WEIGHT
           "name": np.array([0, 0, 1.5, 0]),
           "who": np.array([0, 0, 1.5, 0]),
           
           # SCHEDUAL INQUIRY ([0, 0, 0, ?]) NON-LINEAR WEIGHT
           "compass": np.array([0, 0, 0, 3.5]),
           "schedule": np.array([0, 0, 0, 3.5]),
           "class": np.array([0, 0, 0, 3.5]),
           "classes": np.array([0, 0, 0, 3.5]),
           }

# (note for me) HUNG REMEMEBR IT STARTS AT 0 NOT 1
response_thingy = {0: greeting,
                   1: insults,
                   2: name_inquiry,
                   3: schedule_inquiry,
                   }

def GetReply(input): # i learnt arguement passing a while back and ye

    for sym in ["!", "?", ".", ",", ";", ":", "(", ")", "[", "]", "{", "}", "\"", "'", "\\", "|", "#", "$", "%", "^", "&", "*", "_", "-", "+", "=", "<", ">", "`", "~"]:
        input = input.replace(sym, "")

    input = input.replace("whats", "what")

    if (input == "whats the time" or input == "what is the time"
        or "what the time" in input):
        now_melbourne = datetime.now(ZoneInfo("Australia/Melbourne"))
        melbourne_time = now_melbourne.strftime("%I:%M %p")
        return(melbourne_time)
    
    input_weight = np.zeros(4) #[0, 0, 0, 0]

    try:
        input.split()
    except:
        return("invalid input (undefined error)")
    
    for words in input.split():
        try:
            input_weight += weights[words]
        except:
            pass
    
    thingy1 = np.max(input_weight)
    thingy2 = 0

    for value in input_weight:
        if value == thingy1:
            thingy2 += 1

    if thingy2 >1:
        return("Intent unclear i cannot answer that")
    
    if np.max(input_weight) < 0.1:
        return("Intent unclear i cannot answer that")

    # you can ignore this note its aslo for me 
    # 1 = greeting, 2 = insult, 3 = name_inquiry, 4 = schedual_inquiry
    response = np.argmax(input_weight)

    return(r.choice(response_thingy[response]))
    # MAIN LOGIC UP THERE

def spellcheck(input2):
    for sym in ["!", "?", ".", ",", ";", ":", "(", ")", "[", "]", "{", "}", "\"", "'", "\\", "|", "#", "$", "%", "^", "&", "*", "_", "-", "+", "=", "<", ">", "`", "~"]:
        input2 = input2.replace(sym, "")
    
    input2 = input2.split()

    for index, words in enumerate(input2):
        if words.lower() not in checker:
            suggestion = checker.correction(words)

            if suggestion != None:
                input2[index] = suggestion

    input2 = " ".join(input2)
    return(input2)

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1) 
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            audio = recognizer.recognize_google(audio)
            return(audio)
        except sr.WaitTimeoutError:
            raise NoInputDetectedError
        except sr.UnknownValueError:
            raise InputUnrecognisedError
        except sr.RequestError:
            raise SeverRequestFailiure
        
def voice_reply(reply):
    tts_engine = tts.init()
    voice = tts_engine.getProperty('voices')
    tts_engine.setProperty('voice', voice[1].id)
    tts_engine.say(reply)
    tts_engine.runAndWait()

THETA = "\u03B8"
NEGATIVE_POWER = "⁻¹"
DEGREE_SYM = "°"
def explain_logic():
    print("""                                      NOTai""")
    print("""                        ----------------------------------""")
    print(f"""
THE LOGIC:
---------
Hello, our chatbot (Hung B(redacted for portfolio), C(redacted for portfolio) N(redacted for portfolio)),
uses the same principle of vectors as real AI's do,
but in such a small scale its basically an advanced
keyword search
---------
so what is the vector system?
in the world of NLP(natural language processing), the
concept of vectors is a multidimentional (well in
this case, 4 dimentions) graph that places every word
in the english dictionary on there, for example, in graph
(x, y), x may represent "food-related-ness" and y may
represent "math-related-ness", so the word "hamburger"
may be (10, 0) and the word "algebra" may be (0, 10), "true"
ai vectors are just like so, yet on a much, much bigger
scale, with a single sentence having upwards of 50 thousand
coordinates (meaning lots of dimentions on the vector graph).

So why is this inportant?
when we "draw" two arrows from the orign (0, 0) to the two word's
coordinates, and then connect them via a line that is exacally 90{DEGREE_SYM}
to one of the lines, conencting the two lines together, this forms
a right-angled triangle, in which we have the exact units for its
adj and its hyp, and, adj/hyp == Cos({THETA}), which also means
Cos{NEGATIVE_POWER}(adj/hyp) == {THETA}, and that very {THETA}
represents how close the two words are in meaning(cosine simmilarity). 
and that there,is one of the two most complex concept at the heart of ai,
with the other being self-learning but im too stoopid to learn that right now.

How do we use this concept?
the libary "Numpy" offers us a new type of list (named the Numpy array) that,
unlike a regular list that, for example:
list1 = [1, 0, 1, 0]
list2 = [0, 1, 0, 1]

print(list1 + list2)

OUTPUT = 1, 0, 1, 0, 0, 1, 0, 1

but a numpy array would return:

OUTPUT = 1, 1, 1, 1

now this little change allows us to make a smaller version of the vector system,
our one has 4 dimentions, and then assign weight to keywords that then add to
the total weight Numpy array that represents the user's input, then, depending on the
infered intent, can then pick a premade response from the dictionary i have assigned
to that intent, else if the intent is unclear it will response with 'intent unclear
i cannot answer that.
""")
    
def print_credit():
    print("""                                      NOTai""")
    print("""                        ----------------------------------""")
    print("""CREDITS
--------------
H(redacted for portfolio) B(redacted for portfolio) - Developer
C(redacted for portfolio) N(redacted for portfolio) - Product Manager
R(redacted for portfolio) V(redacted for portfolio) B(redacted for portfolio) - inspired the speaker identifiers by telling me to do it
--------------
LIBARIES AND MODUELS
-The os module
-The time module
-The random module
-The datetime module
-The zoneinfo module
-The numpy library
-The sounddevice library
-The pyspellchecker library
-The pyttsx3 library
--------------
""")
    
def print_feature():
    print("""                                      NOTai""")
    print("""                        ----------------------------------""")
    print("""FEATURES:
Text-To-Speech
Voice Input
Spell Checking (flawed, cannot reconise names)""")
