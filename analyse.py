def mood_detector(text):
    if 'хорошее' or 'хорошо' in text.lower():
        return 'good'
    elif 'Плохое' or 'Плохо' in text.lower():
        return 'bad'
    else:
        return 'ERR1'


def emotion_detector(text):
    if 'экстаз' or 'восхищение' or 'изумление' in text.lower():
        return 'mode1'
    elif 'ярость' or 'Отвращение' or 'горе' or 'ужас' in text.lower():
        return 'mode2'
    else:
        return 'ERR1'


def detect_mode(text):
    if 'энергичный' in text.lower():
        return 'ENM'
    elif 'успокаивающий' in text.lower():
        return 'CHLM'
    else:
        return 'ERR1'
