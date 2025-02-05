from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Person, Address, Employee
from flask_login import login_user, login_required, logout_user, current_user
from .views import home

auth = Blueprint('auth', __name__)


@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        employee_id= request.form.get('employee_id')
        password = request.form.get('password')

        employee= Employee.query.filter_by(employee_id=employee_id).first()

        if employee:
            if check_password_hash(employee.password, password):
                login_user(employee,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('ID does not exist.', category='error')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/success')
def success():
    employee_id = request.args.get('employee_id')
    return render_template('success.html',employee_id=employee_id)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        suffix=request.form.get('suffix')
        contact = request.form.get('phoneNo')
        gender = request.form.get('gender')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('confirmPassword')
        birth_date = request.form.get('birthDate')
        house_no = request.form.get('houseNo')
        street = request.form.get('street')
        barangay = request.form.get('barangay')
        city = request.form.get('city')
        province = request.form.get('province')
        postal_code = request.form.get('postalCode')
        employment_date=request.form.get('employmentDate')
        employee_type=request.form.get('employeeType')

        emailcheck= Person.query.filter_by(email_address=email).first()
        contactcheck=Person.query.filter_by(contact_number=contact).first()

        if emailcheck:
            flash('Email already exist!', category='error')
        if contactcheck:
            flash('Contact number already exist!', category='error')
        elif len(first_name)<2:
            flash('First Name must be greater than 1 character!', category='error')
        elif not first_name.isalpha():
            flash('First Name must only contain letters in the alpabet', category='error')
        elif len(last_name)<2:
            flash('Last Name must be greater than 1 character!', category='error')
        elif not last_name.isalpha():
            flash('Last Name must be greater than 1 character!', category='error')
        elif gender=='Gender':
            flash('Please select a gender!', category='error')
        elif not contact.isdigit():
            flash('Contact number must be in digits!', category='error')
        elif not len(contact)==11:
            flash('Contact number must have 11 digits!', category='error')
        elif len(email)<3:
            flash('Email must be greater than 3 characters!', category='error')
        elif len(password)<8:
            flash('Password must be at least 8 characters!', category='error')
        elif password!=password2:
            flash('Password dont match!', category='error')
        elif birth_date=='':
            flash('Please enter Date of Birth!', category='error')
        elif len(house_no)>100:
            flash('House/Building Number length too long!', category='error')
        elif len(barangay)>100:
            flash('Barangay length too long!', category='error')
        elif len(city)>100:
            flash('City length too long!', category='error')
        elif len(province)>100:
            flash('Province length too long!', category='error')
        elif not postal_code.isdigit():
            flash('Postal code must be in digits!', category='error')
        elif employment_date == '':
            flash('Please enter Date of Birth!', category='error')
        elif employee_type=='Employment Status':
            flash('Please enter Employment Status!', category='error')
        else:
            new_address = Address(loc_number = house_no, street_name=street, barangay=barangay, city=city, province=province, postal_code=postal_code)

            db.session.add(new_address)
            db.session.commit()
            
            address_id = new_address.id

            if gender=='1':
                new_person = Person(first_name=first_name, last_name=last_name, name_append=suffix, contact_number=contact, is_male=True, email_address=email,
                                date_of_birth=birth_date,address_id=address_id)
            else:
                new_person = Person(first_name=first_name, last_name=last_name, name_append=suffix, contact_number=contact, is_male=False,email_address=email,
                                date_of_birth=birth_date,address_id=address_id)
            
            db.session.add(new_person)
            db.session.commit()

            person_id  = new_person.id

            employment_date2 = datetime.strptime(employment_date, '%Y-%m-%d')
            employment_year = employment_date2.year
            employee_id = f"WRL{employment_year}{person_id}"

            if employee_type=='2':
                new_employee = Employee(id=person_id, employee_id=employee_id, date_employed=employment_date,password=generate_password_hash(password,method='pbkdf2:sha1'), is_senior=True,)
            else:
                new_employee = Employee(id=person_id, employee_id=employee_id, date_employed=employment_date,password=generate_password_hash(password,method='pbkdf2:sha1'), is_senior=False)

            db.session.add(new_employee)
            db.session.commit()
            
            return redirect(url_for('auth.success',employee_id=employee_id))        
          
    return render_template('register.html')
