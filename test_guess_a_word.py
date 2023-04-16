"""
Homework: Test Guess a Word
===========================
Course:   CS 5001
Student:  Chanyuan Liu
Semester: Spring 2023
"""
from guess_a_word import recognize_speech_from_file, get_guess,\
    load_filenames_from_file 

import unittest
import speech_recognition as sr

class CrashTest(unittest.TestCase):
    """Tests guess_a_word.py by calling functions in it, and
    making sure the values of the attributes are what we expect.
    """    
    def test_recognize_speech_from_file_1(self) -> None:
        """Tests recognize_speech_from_file function with apple.wav"""
        test_recognizer = sr.Recognizer()
        test_dict = recognize_speech_from_file(test_recognizer, 'apple.wav')
        expected = {'success': True, 'error': None, 'transcription': 'apple'}
        self.assertEqual(test_dict, expected)

    def test_recognize_speech_from_file_2(self) -> None:
        """Tests recognize_speech_from_file function with 'Unknown'"""
        test_recognizer = sr.Recognizer()
        test_dict = recognize_speech_from_file(test_recognizer, 'Unknown')
        expected = {'success': True,
                    'error': 'You need to choose a plant from the list.',
                    'transcription': None}
        self.assertEqual(test_dict, expected)

    def test_recognize_speech_from_file_raises_type_error(self) -> None:
        """Tests recognize_speech_from_file function raises a TypeError"""
        test_recognizer = 1
        with self.assertRaises(TypeError):
            recognize_speech_from_file(test_recognizer, 'apple.wav')

    def test_recognize_speech_from_file_raises_value_error(self) -> None:
        """Tests recognize_speech_from_file function raises a ValueError"""
        test_recognizer = sr.Recognizer()
        with self.assertRaises(ValueError):
            recognize_speech_from_file(test_recognizer, 'audio_files.csv')

    def test_recognize_speech_from_file_except_unknown_value_error(self)\
        -> None:
        """Tests recognize_speech_from_file function excepts an
        UnknownValueError
        """
        test_recognizer = sr.Recognizer()
        test_dict = recognize_speech_from_file(test_recognizer,\
                    'whitenoisegaussian.wav')
        expected = {'success': True,
                    'error': 'Unable to recognize speech',
                    'transcription': None}
        self.assertEqual(test_dict, expected)

    def test_load_filenames_from_file(self):
        """Tests load_filenames_from_file function with a simple_file.csv"""
        ## pass in simple_file.csv
        filename = 'a.csv'
        test_list = load_filenames_from_file('a.csv')
        expected = ['a', '1', '2']
        self.assertEqual(test_list, expected)        

    def test_get_guess(self):
        """Tests get_guess by choosing rose.wav"""
        test_recognizer = sr.Recognizer()
        i = 0
        transcription = get_guess(test_recognizer, i)
        self.assertEqual(transcription, 'rose')

    def test_get_guess_unknown_value_error_max_times(self):
        """Tests get_guess with test.wav which is 
        whitenoisegaussian for maximum times"""
        test_recognizer = sr.Recognizer()
        i = 0
        filenames = 'test_audio_files.csv'
        transcription = get_guess(test_recognizer, i, filenames)
        self.assertEqual(transcription, None)

    def test_get_guess_wrong_file_names_max_times(self):
        """Tests get_guess with wrong plant names for maximum times"""
        test_recognizer = sr.Recognizer()
        i = 0
        transcription = get_guess(test_recognizer, i)
        self.assertEqual(transcription, None)


def main():
    unittest.main(verbosity = 3)

main()
