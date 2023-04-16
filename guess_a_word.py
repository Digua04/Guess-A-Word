"""
guess_a_word uses speech recognition to create a word-guessing game.
The computer chooses a random word from a CSV file, and players must
guess the word by selecting an audio file in **.wav format.

NAME: Chanyuan Liu
SEMESTER: Spring 2023
"""
import speech_recognition as sr
import random
import time
import csv

_MAX_GUESSES = 3
_PROMPT_LIMIT = 5


def recognize_speech_from_file(recognizer, filename='Unknown') -> dict:
    """Transcribes speech from an audio file.

    See:
        https://pypi.org/project/SpeechRecognition/

    Arguments:
        recognizer (speech_recognition.Recognizer)
        filename (str): the selected audio file name

    Returns:
        dict:
            "success":  a boolean indicating whether or not the API request is
                        successful
            "error":    'None' if no error occurs, otherwise a string
                        containing an error message if the API could not be
                        reached or speech is unrecognizable
            "transcription": 'None' if speech can not be transcribed, otherwise
                        a string containing the transcribed text
    """
    # check the recognizer is appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError

    # set up the response object
    response = {
        'success': True,
        'error': None,
        'transcription': None
    }

    # check if the filename is in the CSV file
    if filename == 'Unknown':
        response['error'] = 'You need to choose a plant from the list.'
        return response

    # check if the file is appropriate type
    guess_audio = sr.AudioFile(filename)
    if not isinstance(guess_audio, sr.AudioFile):
        raise ValueError

    # adjust the recognizer sensitivity to ambient noise
    with guess_audio as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.05)
        contents = recognizer.record(source, duration=2)

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    # update the response object accordingly
    try:
        response['transcription'] = recognizer.recognize_google(contents)\
            .lower()
    except sr.RequestError:  # API was unreachable or unresponsive
        response['success'] = False
        response['error'] = 'API unavailable'
    except sr.UnknownValueError:  # speech was unintelligible
        response['error'] = 'Unable to recognize speech'
    return response


def load_filenames_from_file(filename: str) -> list:
    """Read the file specified by filename, and return a list of
       audio file names.

    Args:
        filename (str): the name of the file that stores the names of audio
        files.

    Returns:
        filenames: a list of audio file names minus the .wav part
    """
    filenames = []
    with open(filename) as csv_file:
        csv_read = csv.reader(csv_file)
        for row in csv_read:
            filenames.append(row[0].removesuffix('.wav'))
    return filenames


def get_guess(recognizer, i, filenames='audio_files.csv') -> str:
    """Get the guess from the user by selecting an audio file name.

    Arguments:
        recognizer: a recognizer instance

    Returns:
        guess[transcription] (str)
    """
    filenames = load_filenames_from_file(filenames)
    for j in range(_PROMPT_LIMIT):
        print(f'Guess {i+1}. Choose!')
        guess_prompt = (
            "Choose a file:\n"
            "{filenames}\n"
        ).format(filenames=', '.join(filenames))
        guess = input(guess_prompt)
        if guess in filenames:
            response = recognize_speech_from_file(recognizer, guess+'.wav')
            if response['transcription']:  # if a transciption is returned
                break
            if not response['success']:  # if API was unreachable
                break
            # if API request succeeded but no transcription was returned,
            # re-prompt the user to say their guess again until up to
            # _PROMPT_LIMIT times.
            print("I didn't catch that. Enter the file name again.\n")
        else:
            response = recognize_speech_from_file(recognizer)
            print('Please enter a correct file name.')
    if response['error']:
        print(f"ERROR: {response['error']}")
    return response['transcription']


if __name__ == '__main__':
    # set the list of words
    filenames = 'audio_files.csv'
    words = load_filenames_from_file(filenames)

    # create recognizer instance
    recognizer = sr.Recognizer()

    # get a random word from the list
    word = random.choice(words)

    # format the instructions string
    instructions = (
        "I'm thinking of one of these words:\n"
        "{words}\n"
        "You have {n} tries to guess which one.\n"
    ).format(words=', '.join(words), n=_MAX_GUESSES)

    # show instructions and wait 3 seconds before starting the game
    print(instructions)
    time.sleep(3)

    # get the guess from the user
    for i in range(_MAX_GUESSES):
        guess_num = i
        guess = get_guess(recognizer, i, filenames)

        # show the user the transcription
        print(f"You said: {guess}")

        # determine if guess is correct and if any attempts remain
        guess_is_correct = guess == word.lower()
        user_has_more_attempts = i < _MAX_GUESSES - 1

        # determine if the user has won the game
        # if not, repeat the loop if user has more attempts
        # if no attempts left, the user loses the game
        if guess_is_correct:
            print("Correct! You win!")
            break
        elif user_has_more_attempts:
            print("Incorrect. Try again.\n")
        else:
            print(f"Sorry, you lose!\nI was thinking of '{word}'.")
            break
