
import unittest
from pwn3dornot import build_url, get_filename, hibp_response, read_emails
TEST_PATH = 'test/'



class Test_Pwn3d_Ornot(unittest.TestCase):
    
    def test_no_filename(self):
        with self.assertRaises(FileNotFoundError):
            get_filename(['script.py', 'file.txt'])
       
    
    def test_empty_file(self):
        with self.assertRaises(ValueError):
            get_filename(['script.py',TEST_PATH + 'exampleempty.txt'])




    def test_get_filename(self):
        first = get_filename(['script.py', TEST_PATH +'example.txt'])
        second = TEST_PATH + 'example.txt'
        self.assertEqual(first, second)


    def test_file_empty(self):
        get_filename(['scripy.py', TEST_PATH + 'example.txt'])
        self.assertTrue

    def test_read_mails(self):
        first = read_emails(TEST_PATH + 'readtest.txt')
        second = ['example@example.com','second@example.com']
        self.assertEqual(first, second)

    def test_build_url(self):
        first = build_url('example@example.com')
        second = 'https://haveibeenpwned.com/api/v3/breachedaccount/example%40example.com?truncateResponse=false'
        self.assertEqual(first, second)

    def test_api_call(self):
        first = hibp_response('https://haveibeenpwned.com/api/v3/breachedaccount/example%40example.com?truncateResponse=false')
        self.assertTrue(len(first) > 0)
      
 

if __name__ == '__main__':
    unittest.main()
