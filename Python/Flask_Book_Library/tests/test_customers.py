import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.customers.models import Customer
from project.customers.views import checker

class CustomerTests(unittest.TestCase):
    
    # Testy poprawnych danych
    valid_cases = [
        {"name": "John Doe", "city": "New York", "age": 30},
        {"name": "Alice Smith", "city": "Los Angeles", "age": 25},
        {"name": "Bob Johnson", "city": "Chicago", "age": 40},
    ]
    
            
    def test_customer_creation_valid(self):
        for data in self.valid_cases:
            customer = Customer(**data)
            self.assertEqual(customer.name, data["name"])
            self.assertEqual(customer.city, data["city"])
            self.assertEqual(customer.age, data["age"])
    
    # Testy niepoprawnych danych
    invalid_cases = [
        {"name": "", "city": "Valid City", "age": 30},  # Puste imię
        {"name": "Valid Name", "city": "", "age": 30},  # Puste miasto
        {"name": "Valid Name", "city": "Valid City", "age": "Not a Number"},  # Zły format wieku
        {"name": "Valid Name", "city": "Valid City", "age": -5},  # Ujemny wiek
        {"name": "Valid Name", "city": "Valid City", "age": 200},  # Wiek poza zakresem
        {"name": "J0hn Doe", "city": "Valid City", "age": 30},  # Niedozwolone znaki w imieniu
        {"name": "Valid Name", "city": "N3w York", "age": 30},  # Niedozwolone znaki w mieście
    ]
    
    def test_customer_creation_invalid(self):
        for data in self.invalid_cases:
            with self.assertRaises(ValueError):
                checker(data["name"], data["city"], data["age"])
    
    # Testy wstrzyknięcia SQL i JavaScript
    sql_js_injection_cases = [
        {"name": "Robert'); DROP TABLE customers;--", "city": "HackerTown", "age": 30},
        {"name": "<script>alert('XSS')</script>", "city": "Malicious", "age": 30},
        {"name": "' OR '1'='1' --", "city": "SQL Attack", "age": 30},
    ]
    
    def test_sql_js_injection(self):
        for data in self.sql_js_injection_cases:
            with self.assertRaises(ValueError):
                checker(data["name"], data["city"], data["age"])
    
    # Testy ekstremalne
    extreme_cases = [
        {"name": "A" * 100, "city": "B" * 100, "age": 50},  # Za długie pola
        {"name": "Short", "city": "City", "age": -1},  # Ujemny wiek
        {"name": "Short", "city": "City", "age": 151},  # Poza zakresem wieku
    ]
    
    def test_extreme_cases(self):
        for data in self.extreme_cases:
            with self.assertRaises(ValueError):
                checker(data["name"], data["city"], data["age"])
    
if __name__ == "__main__":
    unittest.main()
