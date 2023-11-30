import unittest
from unittest.mock import Mock, patch, call
from app import App

class TestApp(unittest.TestCase):
    def setUp(self):
        self.mock_ref_service = Mock()
        self.mock_io = Mock()
        self.app = App(self.mock_ref_service, self.mock_io)

    def test_add_book_short_command(self):
        self.mock_io.read.side_effect = ['a', 'b', 'Author Name', 'Book Title', '2023',
                                          'Publisher Name', '', '']
        self.app.run()
        self.mock_ref_service.create_reference.assert_called_once_with(
            'book', ['Author Name', 'Book Title', '2023', 'Publisher Name', '']
        )
        self.mock_io.write.assert_any_call("Reference type book added")

    def test_add_book_full_command(self):
        self.mock_io.read.side_effect = ['add', 'book', 'Author Another', 'Second Book Title',
                                          '2123', 'Another Publisher', '', '']
        self.app.run()
        self.mock_ref_service.create_reference.assert_called_once_with(
            'book', ['Author Another', 'Second Book Title', '2123', 'Another Publisher', '']
        )
        self.mock_io.write.assert_any_call("Reference type book added")

    def test_print_short_command(self):
        self.mock_io.read.side_effect = ['p', '']
        # Just return something, not testing for reference validity
        mock_references = ['  Type: book\n  Author: Author Name\n  Title: Book Title\
            \n  Publication date: 2023\n  Publisher: Publisher Name\n']
        self.mock_ref_service.print_refs.return_value = mock_references

        self.app.run()
        self.mock_ref_service.print_refs.assert_called_once()
        # Need to test that the return value is correct

    def test_create_bib_short_command(self):
        self.mock_io.read.side_effect = ['c', '']

        self.app.run()
        self.mock_ref_service.create_bib_format_file.assert_called_once()
        # Just testing for calling of create_bib

if __name__ == '__main__':
    unittest.main()
