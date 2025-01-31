from flask import render_template, Blueprint, request, redirect, url_for, jsonify
from project import db
from project.customers.models import Customer
import bleach
import re

def checker(name, city, age):
    try:
        age = int(age)
    except ValueError:
        raise ValueError("Age must be an integer value")

    if age < 0 or age > 150:
        raise ValueError("Age must be between 0 and 150")

    if not (1 <= len(name) <= 50):
        raise ValueError("Customer name must contain 1-50 characters")
    if not (1 <= len(city) <= 50):
        raise ValueError("City must contain 1-50 characters")
    if not re.match(r"^[a-zA-Z\s]+$", name):
        raise ValueError("Customer name must only contain letters and spaces")
    if not re.match(r"^[a-zA-Z\s]+$", city):
        raise ValueError("City must only contain letters and spaces")

# Blueprint for customers
customers = Blueprint('customers', __name__, template_folder='templates', url_prefix='/customers')

# Funkcja do czyszczenia danych wejściowych
def sanitize_input(value):
    return bleach.clean(value, strip=True)

# Route to display customers in HTML
@customers.route('/', methods=['GET'])
def list_customers():
    customers = Customer.query.all()
    print('Customers page accessed')
    return render_template('customers.html', customers=customers)

# Route to fetch customers in JSON format
@customers.route('/json', methods=['GET'])
def list_customers_json():
    customers = Customer.query.all()
    customer_list = [{'name': customer.name, 'city': customer.city, 'age': customer.age} for customer in customers]
    return jsonify(customers=customer_list)

# Route to create a new customer
@customers.route('/create', methods=['POST', 'GET'])
def create_customer():
    data = request.form

    if 'name' not in data or 'city' not in data or 'age' not in data:
        print('Invalid form data')
        return jsonify({'error': 'Invalid form data'}), 400

    try:
        # Sanityzacja danych wejściowych
        sanitized_name = sanitize_input(data['name'])
        sanitized_city = sanitize_input(data['city'])
        sanitized_age = data['age']
        
        checker(sanitized_name, sanitized_city, sanitized_age)

        new_customer = Customer(name=sanitized_name, city=sanitized_city, age=sanitized_age)
    except Exception as e:
        return jsonify({'error': f'{str(e)}'}), 400

    try:
        db.session.add(new_customer)
        db.session.commit()
        print('Customer added successfully')
        return redirect(url_for('customers.list_customers'))
    except Exception as e:
        db.session.rollback()
        print('Error creating customer')
        return jsonify({'error': f'Error creating customer: {str(e)}'}), 500

# Route to fetch customer data for editing
@customers.route('/<int:customer_id>/edit-data', methods=['GET'])
def edit_customer_data(customer_id):
    customer = Customer.query.get(customer_id)

    if customer:
        customer_data = {
            'name': customer.name,
            'city': customer.city,
            'age': customer.age
        }
        return jsonify({'success': True, 'customer': customer_data}), 200
    else:
        print('Customer not found')
        return jsonify({'error': 'Customer not found'}), 404

# Route to update an existing customer
@customers.route('/<int:customer_id>/edit', methods=['POST'])
def edit_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if not customer:
        print('Customer not found')
        return jsonify({'error': 'Customer not found'}), 404

    try:
        data = request.form

        # Sanityzacja danych wejściowych
        customer.name = sanitize_input(data['name'])
        customer.city = sanitize_input(data['city'])
        customer.age = data['age']
        
        checker(customer.name, customer.city, customer.age)

        db.session.commit()
        print('Customer updated successfully')
        return redirect(url_for('customers.list_customers'))
    except Exception as e:
        db.session.rollback()
        print('Error updating customer')
        return jsonify({'error': f'Error updating customer: {str(e)}'}), 500

# Route to delete a customer
@customers.route('/<int:customer_id>/delete', methods=['POST'])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        print('Customer not found')
        return jsonify({'error': 'Customer not found'}), 404

    try:
        db.session.delete(customer)
        db.session.commit()
        print('Customer deleted successfully')
        return redirect(url_for('customers.list_customers'))
    except Exception as e:
        db.session.rollback()
        print('Error deleting customer')
        return jsonify({'error': f'Error deleting customer: {str(e)}'}), 500
