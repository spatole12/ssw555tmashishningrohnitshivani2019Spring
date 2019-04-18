import unittest
import timedelta
import datetime
from us_ny import us01_tsk01_is_b4_now

class TestProject(unittest.TestCase):
    #pre-condition: date string format is correct if date is available
    def test_us01_tsk01_is_b4_now(self):
        # if date is not available, it is considered as true
        self.assertTrue(us01_tsk01_is_b4_now("NA"))
        # if date is before current date, it is true
        self.assertTrue(us01_tsk01_is_b4_now("1990-12-18"))
        self.assertTrue(us01_tsk01_is_b4_now("1980-02-13"))
        # if date is after current date, it is false
        futureDate = datetime.datetime.now() + datetime.timedelta(days = 60)
        self.assertFalse(us01_tsk01_is_b4_now(futureDate.strftime('%Y-%m-%d')))
        futureDate = datetime.datetime.now() + datetime.timedelta(days = 365)
        self.assertFalse(us01_tsk01_is_b4_now(futureDate.strftime('%Y-%m-%d')))

if __name__ == '__main__':
    unittest.main()