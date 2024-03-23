from flask import Flask, render_template, request, redirect, url_for
from signup import signUpForm
from product import ProductForm
import datetime, random
from faker import Faker

app = Flask(__name__)
Faker.seed(0)
fake = Faker()
app.config['SECRET_KEY'] = 'secret'


def generate_profile(num_profiles):
    profiles = []

    for _ in range(num_profiles):
        profile = fake.profile()
        profiles.append(profile)
    return profiles


def generate_product(num_products):
    products = []
    for i in range(num_products):
        product_name = fake.company()
        short_description = fake.catch_phrase()
        category = fake.word()
        price = round(random.randint(10, 1000), 2)

        product_id = i + 1
        products.append({
            'id': product_id,
            'name': product_name,
            'short_description': short_description,
            'category': category,
            'price': price,
        })
    return products


# Global variable
product_data = generate_product(200)
cart = []


@app.route("/")
def home():
    return render_template('index.html', title='Home', description='This is home template')


@app.route("/profile")
def profile():
    time = datetime.datetime.now()
    profile_data = generate_profile(50)
    return render_template('profile.html', title='Profile', description='This is Profile page', profiles=profile_data,
                           time=time)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = signUpForm()

    if request.method == 'POST':
        form = signUpForm(request.form)
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            phone = form.phone.data
            gender = form.gender.data
            username = form.username.data
            password = form.password.data

            print(f"Name: {name}")
            print(f"Email: {email}")
            print(f"Phone: {phone}")
            print(f"Gender: {gender}")
            print(f"Username: {username}")
            print(f"Password: {password}")
            return 'Registration successful!'

    return render_template('signup.html', title='signup', form=form)


@app.route("/product")
def product():
    blank_product_form = ProductForm()
    form = ProductForm()
    return render_template('product.html', title='product', form=form, products=product_data,
                           blank_product_form=blank_product_form)


@app.route("/add_to_cart/<product_id>", methods=['GET', 'POST'])
def add_to_cart(product_id):
    product_id = int(product_id)
    form = ProductForm(request.form)
    blank_product_form = ProductForm({})

    if request.method == 'POST':
        if form.validate_on_submit():
            for product in product_data:
                if product['id'] == product_id:
                    variant = form.variant.data
                    quantity = form.quantity.data
                    product_in_cart = product.copy()
                    product_in_cart.update({'variant': variant, 'quantity': quantity})
                    cart.append(product_in_cart)
                    return redirect("/cartList")
            print(f"{product_id} Product ID not found.")
    print(form.errors)
    return render_template('product.html', title='product', products=product_data,
                           blank_product_form=blank_product_form, form=form, product_id=product_id)


@app.route("/cartList")
def cartList():
    price = 0
    for c in cart:
        price += c['price'] * c['quantity']

    return render_template("cartlist.html", title="Cart List", cart=cart, totalprice=price)


if __name__ == "__main__":
    app.run(use_reloader=True, debug=True)
