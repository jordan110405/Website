from flask import Blueprint, request, render_template, session, flash, redirect, url_for, current_app, \
    send_from_directory, jsonify
from myapp import db, create_app
from .models import lost_and_found, UserInfo, Products
from .forms import ProductForm, lost_and_found_form
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
import os
from werkzeug.utils import secure_filename
import random

bp = Blueprint('bp', __name__, static_folder='',
               static_url_path='/static')  # bp = Blueprint('bp', __name__, static_folder='static', static_url_path='/static')
UPLOAD_FOLDER = "myapp/static/uploads"
UPLOAD_FOLDER_LAF = 'myapp/static/uploads-laf'


@bp.route("/")
def index():
    user_id = session.get('existing_user_login.id')
    products = Products.query.all()

    if user_id:
        info = UserInfo.query.filter_by(id=user_id).first()
        if info:
            user_info = info.username
            return render_template('index.html', products=products, user_info=user_info)
        else:
            return "User info not found", 404
    else:
        return render_template('index.html', products=products)



@bp.route("/donate-item", methods=["GET"])
def donateItem():
    form = ProductForm()
    return render_template("donate-item.html", form=form)

@bp.route("/<productID>", methods=['GET', 'POST'])
def product_ind(productID):
    info = Products.query.filter_by(id=productID).first()
    return render_template("product-index.html", info=info)


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("signup-username")
        password = request.form.get("signup-password")
        email = request.form.get("signup-email")
        phone_number = request.form.get("signup-phone-number")
        location = request.form.get("signup-location")

        existing_user = UserInfo.query.filter_by(username=username).first()
        existing_email = UserInfo.query.filter_by(email=email).first()

        if phone_number:
            # If a phone number is provided, check if it already exists
            existing_phone_number = UserInfo.query.filter_by(phone_number=phone_number).first()
            if existing_phone_number:
                flash("Phone number is already registered.")
                return redirect(url_for('bp.index'))

        if existing_user:
            flash("Username is already taken.")
        elif existing_email:
            flash("Email is already registered.")
        else:
            new_user = UserInfo(username=username, password=password, email=email, phone_number=phone_number,
                                location=location)
            db.session.add(new_user)
            db.session.commit()
            session['logged_in'] = True
            flash("Registration complete. Log In now.")

    return redirect(url_for('bp.index'))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("login-username")
        password = request.form.get("login-password")

        existing_user_login = UserInfo.query.filter_by(username=username).first()

        if existing_user_login and existing_user_login.check_password(password):
            session['existing_user_login.id'] = existing_user_login.id
            flash('Login successful!')
            print('Login successful!')
            session['logged_in'] = True
            return redirect(url_for('bp.index'))
        else:
            flash("Username/email or password incorrect")

    return redirect(url_for('bp.index'))


@bp.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('bp.index'))


@bp.route("/donate-item", methods=['GET', 'POST'])
def upload_product():
    form = ProductForm()
    if form.validate_on_submit():
        name = form.name.data
        details = form.details.data
        pickup_location = form.pickup_location.data
        contact_info = form.contact_info.data
        rad_type = form.rad_type.data
        category = form.category.data

        # Handle file upload
        picture = form.picture.data
        if picture:
            record_count = db.session.query(Products).count()
            filename = secure_filename(str(record_count) + ".png")
            # UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER'] = 'myapp/static/uploads'
            target_dir = "myapp/static/uploads"
            image_path = os.path.join(target_dir, filename)
            picture.save(image_path)
        else:
            image_path = None

        new_product = Products(
            name=name,
            details=details,
            picture=filename,  # Save the file path to the database
            pickup_location=pickup_location,
            contact_info=contact_info,
            rad_type=rad_type,
            category=category,
        )

        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('bp.index'))
    return render_template("donate-item.html", form=form)

@bp.route('/uploads-laf/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER_LAF'], filename)


@bp.route('/<filename_ind>')
def uploaded_thing(filename_ind):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename_ind)

@bp.route('/get_items/<category>')
def get_items(category):
    # Query the database to fetch items based on the category
    # For example, assuming you have a model named 'Item' with a 'category' field
    items = Products.query.filter_by(category=category).all()

    # Convert items to a list of dictionaries (or any other format you prefer)
    items_list = [{'name': item.name, 'category': item.category} for item in items]

    # Return the items as JSON response
    return jsonify(items_list)