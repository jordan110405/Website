from flask import Blueprint, request, render_template, session, flash, redirect, url_for, current_app, \
    send_from_directory, jsonify
from myapp import db, create_app
from .models import lost_and_found, UserInfo, Products, ProductsService
from .forms import ProductForm, lost_and_found_form
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
import os
from werkzeug.utils import secure_filename
import traceback

bp = Blueprint('bp', __name__, static_folder='',
               static_url_path='/static')  # bp = Blueprint('bp', __name__, static_folder='static', static_url_path='/static')
UPLOAD_FOLDER = "myapp/static/uploads"
UPLOAD_FOLDER_LAF = 'myapp/static/uploads-laf'

@bp.route("/")
def index():
    return render_template('index.html')

@bp.route("/item")
def item():
    user_id = session.get('existing_user_login.id')
    products = Products.query.all()
    if user_id:
        info = UserInfo.query.filter_by(id=user_id).first()
        if info:
            user_info = info.username
            return render_template('item.html', products=products, user_info=user_info)
    return render_template('item.html', products=products)
    

@bp.route('/get_all_items', methods=['GET'])
def get_all_items():
    try:
        products = Products.query.all()
        products_list = [{'id': product.id, 'name': product.name, 'picture': product.picture, 'blue': product.blue, 'details': product.details} for product in products]
        return jsonify(products_list)
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'An internal server error occurred'}), 500
    
@bp.route('/get_all_items_service', methods=['GET'])
def get_all_items_service():
    try:
        products = ProductsService.query.all()
        products_list = [{'id': product.id, 'name': product.name, 'picture': product.picture, 'blue': product.blue, 'details': product.details} for product in products]
        return jsonify(products_list)
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'An internal server error occurred'}), 500


@bp.route("/service")
def service():
    user_id = session.get('existing_user_login.id')
    products = ProductsService.query.all()
    if user_id:
        info = UserInfo.query.filter_by(id=user_id).first()
        if info:
            user_info = info.username

            return render_template('service.html', products=products, user_info=user_info)
    return render_template('service.html', products=products)



@bp.route("/donate-item", methods=["GET"])
def donateItem():
    form = ProductForm()
    return render_template("item-form.html", form=form)

@bp.route("/service-item", methods=["GET"])
def serviceItem():
    form = ProductForm()
    return render_template("service-form.html", form=form)

@bp.route("/items/<productID>", methods=['GET', 'POST'])
def product_ind(productID):
    info = Products.query.filter_by(id=productID).first()
    return render_template("product-item.html", info=info)

@bp.route("/service/<productID>", methods=['GET', 'POST'])
def product_indService(productID):
    info = ProductsService.query.filter_by(id=productID).first()
    return render_template("service-item.html", info=info)


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
            session['existing_user_login.id'] = new_user.id 
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


@bp.route("/donate-item", methods=["GET", "POST"])
def upload_product():
    form = ProductForm()
    if form.validate_on_submit():
        name = form.name.data
        details = form.details.data
        pickup_location = form.pickup_location.data
        contact_info = form.contact_info.data
        rad_type = form.rad_type.data
        category = form.category.data
        green = form.green_caps.data
        blue = form.blue_caps.data
        total_blue = blue + (green * 4)

        # Handle file upload
        picture = form.picture.data
        if picture:
            record_count = db.session.query(Products).count()
            filename = secure_filename(str(record_count) + ".png")
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            picture.save(image_path)
        else:
            filename = None

        if rad_type.lower() == "items":
            new_product = Products(
                name=name,
                details=details,
                picture=filename,
                pickup_location=pickup_location,
                contact_info=contact_info,
                rad_type=rad_type,
                category=category,
                blue=total_blue,
            )
            db.session.add(new_product)
            db.session.commit()
            return redirect(url_for('bp.item'))
        else:
            new_service = ProductsService(
                name=name,
                details=details,
                picture=filename,
                pickup_location=pickup_location,
                contact_info=contact_info,
                rad_type=rad_type,
                category=category,
                blue=total_blue,
            )
            db.session.add(new_service)
            db.session.commit()
            return redirect(url_for('bp.service'))

    return render_template("item-form.html", form=form)

@bp.route('/uploads-laf/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER_LAF'], filename)


@bp.route('/<filename_ind>')
def uploaded_thing(filename_ind):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename_ind)

@bp.route('/get_items/<category>')
def get_items(category):
    # Query the database to fetch items based on the category
    if category == "all":
        items = Products.query.all()
        items_list = [{'id': item.id, 'name': item.name, 'picture': item.picture, 'blue': item.blue, 'details': item.details} for item in items]
        return jsonify(items_list)
    
    items = Products.query.filter_by(category=category).all()

    # Convert items to a list of dictionaries
    items_list = [{'id': item.id, 'name': item.name, 'picture': item.picture, 'blue': item.blue, 'details': item.details} for item in items]

    # Return the items as JSON response
    return jsonify(items_list)

@bp.route('/service/get_items/<category>')
def service_get_items(category):
    # Query the database to fetch items based on the category
    if category == "all":
        items = ProductsService.query.all()
        items_list = [{'id': item.id, 'name': item.name, 'picture': item.picture, 'blue': item.blue, 'details': item.details} for item in items]
        return jsonify(items_list)
    
    items = ProductsService.query.filter_by(category=category).all()

    # Convert items to a list of dictionaries
    items_list = [{'id': item.id, 'name': item.name, 'picture': item.picture, 'blue': item.blue, 'details': item.details} for item in items]

    # Return the items as JSON response
    return jsonify(items_list)


@bp.route('/search/<query>', methods=['GET'])
def search(query):
    try:
        # Query the database to find products where title or description contains the query
        results = Products.query.filter((Products.name.like(f'%{query}%')) | (Products.details.like(f'%{query}%'))).all()

        # Convert results to a list of dictionaries
        results_list = [{'id': result.id, 'name': result.name, 'blue': result.blue, 'picture': result.picture, 'details': result.details} for result in results]

        return jsonify(results_list)
    except Exception as e:
        traceback.print_exc()  # This will print the traceback to the console for debugging
        return jsonify({'error': 'An internal server error occurred'}), 500


@bp.route('/service/search/<query>', methods=['GET'])
def search_service(query):
    try:
        # Query the database to find products where title or description contains the query
        results = ProductsService.query.filter((ProductsService.name.like(f'%{query}%')) | (ProductsService.details.like(f'%{query}%'))).all()

        # Convert results to a list of dictionaries
        results_list = [{'id': result.id, 'name': result.name, 'blue': result.blue, 'picture': result.picture, 'details': result.details} for result in results]

        return jsonify(results_list)
    except Exception as e:
        traceback.print_exc()  # This will print the traceback to the console for debugging
        return jsonify({'error': 'An internal server error occurred'}), 500
