import unittest
from project.books.models import Book
from project.books.views import checker

class BookTests(unittest.TestCase):
    
    # Testy poprawnych danych
    valid_cases = [
        {"name": "The Hobbit", "author": "J.R.R. Tolkien", "year_published": 1937, "book_type": "Fantasy"},
        {"name": "Dune", "author": "Frank Herbert", "year_published": 1965, "book_type": "Science Fiction"},
        {"name": "War and Peace", "author": "Leo Tolstoy", "year_published": 1869, "book_type": "Historical"},
    ]
    
    def test_book_creation_valid(self):
        for data in self.valid_cases:
            book = Book(**data)
            self.assertEqual(book.name, data["name"])
            self.assertEqual(book.author, data["author"])
            self.assertEqual(book.year_published, data["year_published"])
    
    
    # Testy niepoprawnych danych
    invalid_cases = [
        {"name": "", "author": "Valid Author", "year_published": 2000, "book_type": "Fiction"},
        {"name": "Valid Name", "author": "", "year_published": 2000, "book_type": "Fiction"},
        {"name": "Valid Name", "author": "Valid Author", "year_published": "Not a Year", "book_type": "Fiction"},
    ]
    
    def test_book_creation_invalid(self):
        for data in self.invalid_cases:
            with self.assertRaises(ValueError):
                checker(data["name"], data["author"], data["year_published"])
    
    # Testy wstrzyknięcia kodu SQL i JavaScript
    sql_js_injection_cases = [
        {"name": "Robert'); DROP TABLE books;--", "author": "Hacker", "year_published": 2023, "book_type": "SQL Injection"},
        {"name": "<script>alert('XSS')</script>", "author": "Malicious User", "year_published": 2023, "book_type": "XSS"},
        {"name": "' OR '1'='1' --", "author": "Hacker", "year_published": 2023, "book_type": "SQL Injection"},
    ]
    
    def test_sql_js_injection(self):
        for data in self.sql_js_injection_cases:
            with self.assertRaises(ValueError):
                checker(data["name"], data["author"], data["year_published"])
    
    # Testy ekstremalne
    extreme_cases = [
        {"name": "A" * 10000, "author": "B" * 10000, "year_published": 9999, "book_type": "Fiction"},
        {"name": "Short", "author": "Author", "year_published": 1000000, "book_type": "Fiction"},
    ]
    
    def test_extreme_cases(self):
        for data in self.extreme_cases:
            with self.assertRaises(ValueError):
                checker(data["name"], data["author"], data["year_published"])
    

if __name__ == "__main__":
    unittest.main()