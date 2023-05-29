# import required libraries
import re
import random
import pyttsx3
import speech_recognition as sr 
import myintents

from nltk.chat.util import reflections
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#initiate speech recognition and TTS engine
recognizer=sr.Recognizer()

engine = pyttsx3.init()
voice = engine.getProperty('voices') #get the available voices
engine.setProperty('voice', voice[1].id) #changing voice to index 1 for female voice

# Function to use NLTK's reflections to check if the user response matches a key in the dictionary
def reflect_input(str_break):
    tokens = str_break.lower().split()
    for j, mytoken in enumerate(tokens):
        if mytoken in reflections:
            tokens[j] = reflections[mytoken]
    return ' '.join(tokens)

# Function to check predefined patterns. If a match is found a random response is selected.
def analyze_input(input_chat):
    for mypattern, myresponses in myintents.pairs:
        match = re.match(mypattern, input_chat.rstrip(".!"))
        if match:
            response = random.choice(myresponses)
            return response.format(*[reflect_input(g) for g in match.groups()])

# Function to print and speak.
def print_and_speak(text, num):
    if num:
        print("Friend :", text)
    else:
        print("You : ", text)
    engine.say(text)
    engine.runAndWait()
    
# Main function
def main():
    # variables
    xyz = ""
    xyz_length = 0
    flag = 0
    chkFlg = 0
    
    # Welcome the user via text and speech.
    print_and_speak("Hi there, welcome my friend. Please express your answers in sentences and not in one or two words!", 1)
    
    print_and_speak("I will be happy to help and support you!", 1)
    
    print_and_speak("And if you want to exit, just say 'good bye'", 1)
    
    print_and_speak("Hello. How are you feeling today?", 1)

    # Continue chat in a continuous while loop
    while True:
        # Get the user speech and convert it to text
        with sr.Microphone() as source:
            # print('Clearing backround noise...')
            recognizer.adjust_for_ambient_noise(source,duration=1)
            print('Waiting for your message...')
            recordedaudio=recognizer.listen(source)
            # print('Done recording...')

        try:
            # print('Printing the message..')
            text=recognizer.recognize_google(recordedaudio,language='en-US')
            print('You: {}'.format(text))
            if 'human' in text: flag=1
        except Exception as ex:
            # In case of exception, print the error and continue.
            print(ex)
            continue

        # Get the user's sentiment from the input.
        Sentence={str(text)}
        analyser=SentimentIntensityAnalyzer()
        for i in Sentence:
            v=analyser.polarity_scores(i)
            # print(v)
        # print(v['neg'])
        # print(v['neu'])
        # print(v['pos'])
        # print(v['compound'])

        if v['compound'] >= 0.05:
            # print("It is a positive statement")
            mood = 'positive'
        elif ((v['compound'] > -0.05) and (v['compound'] < 0.05)):
            # print("It is a neutral statement")
            mood = 'neutral'
        elif v['compound'] <= -0.05:
            # print("It is a negative statement")
            mood = 'negative'
        else:
            # print("Can't find it!")
            mood = 'neutral'
        
        # Process the message.
        #input_chat = input("> ")
        input_chat = str(text)
        if input_chat != "goodbye":
            xyz = xyz +" "+ input_chat
            # print (input_chat,":goodbye:")
            if mood == 'negative':
                input_chat = 'negative ' + input_chat
            vari = analyze_input(input_chat)
            print_and_speak(vari,1)
        else:
            #if input_chat == "goodbye":
            xyz_length = len(xyz.split())
            if ((xyz_length >= 31) or (flag == 1) or (chkFlg == 1)):
                text_file = open("Output.txt", "w")
                text_file.write(xyz)
                text_file.close()
                #print ("Analyzing your responses...")
                #print (xyz_length)
                print_and_speak("Good bye then!",1)
                break
            else:
                print_and_speak("I think I need to chat a bit more with you to help you.",1)
                print_and_speak("So, can we talk more? Tell me a bit more about you.",1)
                print_and_speak("Or, if you want to get support from a human, Please say human help.",1)
                print_and_speak("Or, say good bye to disconnect this chat.",1)
                chkFlg = 1
                continue;

if __name__ == "__main__":
    main()