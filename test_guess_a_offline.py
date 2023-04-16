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
    """Tests guess_a_word.py with no access to networks, and
    making sure the values of the attributes are what we expect.
    """    
    def test_recognize_speech_from_file_except_request_error(self) -> None:
        """Tests recognize_speech_from_file function excepts a RequestError"""
        test_recognizer = sr.Recognizer()
        test_dict = recognize_speech_from_file(test_recognizer, 'peony.wav')
        expected = {'success': False,
                    'error': 'API unavailable',
                    'transcription': None}
        self.assertEqual(test_dict, expected)


def main():
    unittest.main(verbosity = 3)

main()
