import unittest
from unittest.mock import patch, mock_open
from src.student import Student


class TestStudent(unittest.TestCase):

    def setUp(self):
        Student.list_of_students = []
        # adding test students
        self.student1 = Student(1, "Hanna", "Wanna")
        self.student2 = Student(2, "Kamil", "Kokos")

    def test_add_student(self):
        Student.add("Wiktor", "Lodowka")

        #checking if new student has been added
        self.assertEqual(len(Student.list_of_students), 3)
        self.assertEqual(Student.list_of_students[2].first_name, "Wiktor")
        self.assertEqual(Student.list_of_students[2].surname, "Lodowka")

    def test_get_student(self):
        #  getting student by ID
        self.assertEqual(Student.get(1), self.student1)
        self.assertEqual(Student.get(2), self.student2)
        self.assertIsNone(Student.get(3))

    def test_load_from_file(self):
        #testing loading students from file
        mock_data = "1,Hanna,Wanna\n2,Kamil,Kokos\n"
        with patch("builtins.open", mock_open(read_data=mock_data)):
            Student.load_from_file("students.csv")
        self.assertEqual(len(Student.list_of_students), 2)
        self.assertEqual(Student.list_of_students[0].first_name, "Hanna")
        self.assertEqual(Student.list_of_students[1].first_name, "Kamil")

    def test_save_to_file(self):
        #testing saving students to file
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            Student.save_to_file("students.csv")

        # testing if file have been saved with correct data
        mock_file.assert_called_once_with("students.csv", mode="w", newline="")
        handle = mock_file()
        handle.write.assert_any_call("1,Hanna,Wanna\r\n")
        handle.write.assert_any_call("2,Kamil,Kokos\r\n")

        #testing if there is only 2 students saved
        self.assertEqual(handle.write.call_count, 2)

if __name__ == "__main__":
    unittest.main()
