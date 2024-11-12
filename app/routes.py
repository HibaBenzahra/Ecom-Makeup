from app import app, login_manager, db
#import os, requests, json
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from .forms import LoginForm, RegisterForm, CheckoutForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, logout_user
from .db_models import db, User, Item
#from itsdangerous import URLSafeTimedSerializer
#import random
#import pywhatkit
#import subprocess
#from app.wtsp import confirmation_code
#from dotenv import load_dotenv




@app.context_processor
def inject_now():
	""" sends datetime to templates as 'now' """
	return {'now': datetime.utcnow()}

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

@app.route("/")
def home():
	items = Item.query.all()
	return render_template("home.html", items=items)

@app.route("/login", methods=['POST', 'GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		email = form.email.data
		user = User.query.filter_by(email=email).first()
		if user == None:
			flash(f'User doesn\'t exist!<br> <a href={url_for("register")}>Register now!</a>', 'error')
			return redirect(url_for('login'))
		elif check_password_hash(user.password, form.password.data):
			login_user(user)
			return redirect(url_for('home'))
		else:
			flash("Email and password incorrect!!", "error")
			return redirect(url_for('login'))
	return render_template("login.html", form=form)

@app.route("/register", methods=['POST', 'GET'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegisterForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			flash(f"User this email already exists!!<br> <a href={url_for('login')}>Login now!</a>", "error")
			return redirect(url_for('register'))
		new_user = User(name=form.name.data,
						email=form.email.data,
						password=generate_password_hash(
									form.password.data,
									method='pbkdf2:sha256',
									salt_length=8),
						phone=form.phone.data)
		db.session.add(new_user)
		db.session.commit()
		flash('Thanks for registering! You may login now.', 'success')
		return redirect(url_for('login'))
	return render_template("register.html", form=form)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))


@app.route("/add/<id>", methods=['POST'])
def add_to_cart(id):
	if not current_user.is_authenticated:
		flash(f'You must login first!<br> <a href={url_for("login")}>Login now!</a>', 'error')
		return redirect(url_for('login'))

	item = Item.query.get(id)
	if request.method == "POST":
		quantity = request.form["quantity"]
		current_user.add_to_cart(id, quantity)
		flash(f'''{item.name} successfully added to the <a href=cart>cart</a>.<br> <a href={url_for("cart")}>view cart!</a>''','success')
		return redirect(url_for('home'))

@app.route("/cart")
@login_required
def cart():
	price = 0
	price_ids = []
	items = []
	quantity = []
	for cart in current_user.cart:
		items.append(cart.item)
		quantity.append(cart.quantity)
		price_id_dict = {
			"price": cart.item.price_id,
			"quantity": cart.quantity,
			}
		price_ids.append(price_id_dict)
		price += cart.item.price*cart.quantity
	return render_template('cart.html', items=items, price=price, price_ids=price_ids, quantity=quantity)

@app.route('/orders')
@login_required
def orders():
	return render_template('orders.html', orders=current_user.orders)

@app.route("/remove/<id>/<quantity>")
@login_required
def remove(id, quantity):
	current_user.remove_from_cart(id, quantity)
	return redirect(url_for('cart'))

@app.route('/item/<int:id>')
def item(id):
	item = Item.query.get(id)
	return render_template('item.html', item=item)

@app.route('/search')
def search():
	query = request.args['query']
	search = "%{}%".format(query)
	items = Item.query.filter(Item.name.like(search)).all()
	return render_template('home.html', items=items, search=True, query=query)


# Route for successful checkout page
@app.route('/checkout_success')
def checkout_success():
    return render_template('success.html')

# Route for failed checkout page
@app.route('/checkout_failure')
def checkout_failure():
    return render_template('failure.html')

#whatsapp
@app.route('/create-checkout-session', methods=['GET', 'POST'])
def create_checkout_session():
    form = CheckoutForm()
    
    

     #   subprocess.run(['python', 'other_script.py'])

    if form.validate_on_submit(): #and form.confirm_code.data == confirmation_code
        return redirect(url_for('checkout_success'))
    else:
        flash("Couldn't Checkout", category='danger')

    return render_template('checkout.html', form=form)