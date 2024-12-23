import unittest
from unittest.mock import patch, mock_open
from src.presence import Attendance
from src.student import Student


class TestAttendance(unittest.TestCase):

    def setUp(self):
        # adding data fir testing
        self.attendance_data = [
            {'id': 1, 'status': 1},
            {'id': 2, 'status': 0}
        ]
        self.attendance = Attendance("2024-10-30", self.attendance_data) #attendance class object
        Student.list_of_students = [
            Student(1, "Hanna", "Wanna"),
            Student(2, "Kamil", "Kokos")
        ]

    def test_save_to_file(self):
        # testing saving attendace to file
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            self.attendance.save_to_file("attendance/2024-10-30.csv")

        mock_file.assert_called_once_with("attendance/2024-10-30.csv", mode="w", newline="")
        handle = mock_file()


        #check if method was written with correct data
        handle.write.assert_any_call("1,1\r\n")
        handle.write.assert_any_call("2,0\r\n")

    def test_load_attendance_from_file(self):
        # tesing loading attendace from file
        mock_data = "1,1\n2,0\n"
        with patch("builtins.open", mock_open(read_data=mock_data)):
            attendance = Attendance.load_attendance_from_file("attendance/2024-10-30.csv")

        self.assertEqual(attendance.date, "attendance/2024-10-30")
        self.assertEqual(attendance.students_attendance[0]['id'], 1)
        self.assertEqual(attendance.students_attendance[0]['status'], 1)
        self.assertEqual(attendance.students_attendance[1]['id'], 2)
        self.assertEqual(attendance.students_attendance[1]['status'], 0)

    def test_load_attendance_file_not_found(self):
        # testing the case, when the file doesn't exist
        with patch("builtins.open",side_effect=FileNotFoundError): #symulacja bralu pliku
            attendance = Attendance.load_attendance_from_file("attendance/2024-10-30.csv")

        self.assertIsNone(attendance) #check if the result of loading data was None


if __name__ == "__main__":
    unittest.main()
