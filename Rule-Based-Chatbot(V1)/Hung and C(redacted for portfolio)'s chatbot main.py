import os
import time
import hungs_chatbot_logic as logic

user_input_raw = 0
voice_req = False
bot_reply = 0
text_history = ["NOTai: Hi, im NOTai, programmed by Hung and Christian"]
while True:
    os.system("cls")
    user_input = 0
    user_input2 = 0

    print("""                                     NOTai""")
    print("""               --------------------------------------------------""")
    for text in text_history:
        print(text)
        print("")
    print("""------------------------------------------------------------------------------
for credits, input '@credit', for info on the logic, input '@logic', for features input '@feature'
leave blank and 'ENTER' to use voice input, response will then be returned in both text to speech and on
the text log.
------------------------------------------------------------------------------
        """)

    user_input = input(">>>:").lower()
    user_input2 = user_input.strip()

    for sym in ["!", "?", ".", ",", ";", ":", "(", ")", "[", "]", "{", "}", "\"", "'", "\\", "|", "#", "$", "%", "^", "&", "*", "_", "-", "+", "=", "<", ">", "`", "~"]:
        user_input2 = user_input2.replace(sym, "")
    os.system("cls")

    if user_input == "@credit":
        logic.print_credit()
        input("'ENTER' to continue")
        continue
    elif user_input == "@logic":
        logic.explain_logic()
        input("'ENTER' to continue")
        continue

    elif user_input == "@feature":
        logic.print_feature()
        input("'ENTER' to continue")
        continue

    if len(user_input) < 1:
        voice_req = True
        os.system("cls")
        print("Recording in 1 second...")
        time.sleep(1)
        os.system("cls")
        print("Recording...")

        try:
            user_input = logic.listen()

        except logic.NoInputDetectedError:
            os.system("cls")
            print("No input was detected")
            input("'ENTER' to continue")
            continue
        
        except logic.InputUnrecognisedError:
            os.system("cls")
            print("Input could not be recognised")
            input("'ENTER' to continue")
            continue

        except logic.SeverRequestFailiure:
            os.system("cls")
            print("Server (Google) request for SpeechRecognition failed")
            input("'ENTER' to continue")
            continue

    user_input_raw = user_input
    user_input = logic.spellcheck(user_input)
    bot_reply = logic.GetReply(user_input)
    
    if voice_req == True:
        logic.voice_reply(bot_reply)
        voice_req = False

    text_history.append(f"User: {user_input_raw}")
    text_history.append(f"NOTai: {bot_reply}")
