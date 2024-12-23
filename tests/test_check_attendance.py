import unittest
from unittest.mock import patch, mock_open
from src.student import Student
from src.check_attendance import CheckAttendance


class TestCheckAttendance(unittest.TestCase):
#create attendance and update attendace
    def setUp(self):
        # adding test data
        Student.list_of_students = [
            Student(1, "Hanna", "Wanna"),
            Student(2, "Kamil", "Kokos")
        ]

    #mocking open
    @patch('builtins.open', new_callable=mock_open)
    #mocking input for attendance status
    @patch('builtins.input', side_effect=['1', '0'])
    def test_create_attendance(self, mock_input, mock_file):
        # create attendance
        CheckAttendance.create("2024-10-30")

        #test if the file has correct data
        mock_file.assert_called_once_with('attendance/2024-10-30.csv', mode='w', newline='')
        handle = mock_file()

        # test if data is correct
        handle.write.assert_any_call("1,1\r\n")
        handle.write.assert_any_call("2,0\r\n")

    # mocking file read
    @patch('builtins.open', new_callable=mock_open, read_data="1,1\r\n2,0\r\n")
    # mocking input for updating attendance
    @patch('builtins.input', side_effect=['0', '1'])
    def test_update_attendance(self, mock_input, mock_file):

        #update attendance
        CheckAttendance.update("2024-10-30.csv")

        # test if file was saved after updating attendance (open to read/save)
        mock_file.assert_any_call('attendance/2024-10-30.csv', mode='r')
        mock_file.assert_any_call('attendance/2024-10-30.csv', mode='w', newline='')

        handle = mock_file()

        # test if data was updated correctly
        handle.write.assert_any_call("1,0\r\n")
        handle.write.assert_any_call("2,1\r\n")


if __name__ == "__main__":
    unittest.main()
