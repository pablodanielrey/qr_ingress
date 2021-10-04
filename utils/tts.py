import pyttsx3


def change_voice(engine, language, gender='VoiceGenderFemale'):
    for voice in engine.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))

if __name__ == '__main__':
    engine = pyttsx3.init()
    engine.setProperty('voice','spanish')
    # engine.say('Código cu!!ere!! válido')
    # engine.say("inválido")
    # engine.say('Podés ingresar')
    engine.say('ANDATE DE ACAAAA COVIDOSO')
    engine.runAndWait()