import requests
import speech_recognition as sr 
import azure.cognitiveservices.speech as speechsdk
bot_message = ""
message=""
speech_config = speechsdk.SpeechConfig(subscription="d412cb4f4e4c4461bd64dad4fb4fd132", region="westeurope")
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)


speech_config.speech_synthesis_voice_name='en-NZ-MollyNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": "Hello"})

print("Bot says, ",end=' ')
for i in r.json():
    bot_message = i['text']
    print(f"{bot_message}")

# Playing the converted file
#subprocess.call(['mpg321', "welcome.mp3", '--play-and-exit'])

while bot_message != "Bye" or bot_message!='thanks':

    r = sr.Recognizer()  # initialize recognizer
    with sr.Microphone() as source:  # mention source it will be either Microphone or audio files.
        print("Speak Anything :")
        audio = r.listen(source)  # listen to the source
        try:
            message = r.recognize_google(audio)  # use recognizer to convert our audio into text part.
            print("You said : {}".format(message))

        except:
            print("Sorry could not recognize your voice")  # In case of voice not recognized  clearly
            continue
    if len(message)==0:
        continue
    print("Sending message now...")

    r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": message})

    print("Bot says, ",end=' ')
    for i in r.json():
        bot_message = i['text']
        print(f"{bot_message}")

    speech_synthesis_result = speech_synthesizer.speak_text_async(bot_message).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(bot_message))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")
    # myobj = gTTS(text=bot_message)
    # myobj.save("welcome.mp3")
    # print('saved')
    # # Playing the converted file
    # #import playsound
    # playsound.playsound(os.getcwd()+'\welcome.mp3', True)
    # os.remove(os.getcwd()+'\welcome.mp3')