import unittest
import spiders.gradespider as gs
import datetime as dt

class TestCalc(unittest.TestCase):
    pass
    #Tests uploadListToCalendar
    # def test_CalendarTest1(self):
    #     sorted_assignments = [('Final Opt-Out: Search Trees', '2024-12-08 23:59:00 -0800'), ('Quiz 16: Monday, December 2', '2024-12-03 23:59:00 -0800'), ('HW 6', '2024-12-03 23:59:00 -0800'), ('Quiz 15: Monday, November 25', '2024-11-26 23:59:00 -0800'), ('Bloom filter project', '2024-11-26 23:59:00 -0800'), ('Quiz 14: Wednesday, November 20', '2024-11-21 23:59:00 -0800'), ('Quiz 12: Wednesday, November 13', '2024-11-14 23:59:00 -0800'), ('HW 5', '2024-11-12 23:59:00 -0800'), ('Quiz 11: Wednesday, November 6', '2024-11-07 23:59:00 -0800'), ('Quiz 10: Wednesday, October 30', '2024-10-31 23:59:00 -0700'), ('Quiz 9: Monday, October 28', '2024-10-29 23:59:00 -0700'), ('HW 4', '2024-10-29 23:59:00 -0700'), ('Kattis Problems', '2024-10-25 23:59:00 -0700'), ('Quiz 8: Wednesday, October 23', '2024-10-24 23:59:00 -0700'), ('HW 3', '2024-10-22 23:59:00 -0700'), ('Quiz 7: Monday, October 21', '2024-10-22 23:59:00 -0700'), ('Quiz 6: Wednesday, October 16', '2024-10-17 23:59:00 -0700'), ('HW 2', '2024-10-15 23:59:00 -0700'), ('Quiz 5: Monday, October 14', '2024-10-15 23:59:00 -0700'), ('Kattis Problem 1: Sailing Friends', '2024-10-14 23:59:00 -0700'), ('Quiz 4: Wednesday, October 9', '2024-10-10 23:59:00 -0700'), ('Quiz 3: Monday, October 7', '2024-10-08 23:59:00 -0700'), ('HW 1', '2024-10-08 23:59:00 -0700'), ('Quiz 2: Wednesday, October 2', '2024-10-03 23:59:00 -0700'), ('Quiz 1: Monday, September 30', '2024-10-01 23:59:00 -0700')]
    #     result_list = gs.CalendarTest(sorted_assignments)
    #     self.assertEqual(result_list, [])

    # def test_CalendarTest2(self):
    #     firstDate = '2025-1-09 23:59:00 -0800'
    #     sorted_assignments = [('A', firstDate)]
    #     result_list = gs.CalendarTest(sorted_assignments)
    #     datetimeFirstDate = dt.datetime.strptime(firstDate, '%Y-%m-%d %H:%M:%S %z')
    #     self.assertEqual(result_list, [datetimeFirstDate])

    # def test_CalendarTest3(self):
    #     todayDate = '2025-1-08 12:48:00 -0800'
    #     sorted_assignments = [('A', todayDate)]
    #     result_list = gs.CalendarTest(sorted_assignments)
    #     datetimeFirstDate = dt.datetime.strptime(todayDate, '%Y-%m-%d %H:%M:%S %z')
    #     self.assertEqual(result_list, [])

    # #Minutesuntilfuturetime
    # def test_minutes1(self):
    #     time_after_52_minutes = dt.datetime.now() + dt.timedelta(minutes=52)
    #     value = gs.minutes_until_future_time(time_after_52_minutes)
    #     self.assertEqual(value, 52)
if __name__ == '__main__':
    unittest.main()