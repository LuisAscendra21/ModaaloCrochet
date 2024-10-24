from flask import Flask, abort, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import base64
import os

db = SQLAlchemy()

def create_app():
    # Application init
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    # Cambia la ruta de la carpeta de subida
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'uploads')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'clave_secreta_para_la_carga_de_imagenes'
    app.config['SQLALCHEMY_POOL_SIZE'] = 20

    # Create the uploads directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)

    return app

app = create_app()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f'<Category {self.name}>'

# Creamos una tabla para cada categoría
class VestidosDeBano(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('vestidos_de_bano', lazy=True))

class CropTops(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('crop_tops', lazy=True))

class Amigurumis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('amigurumis', lazy=True))

class Detalles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('detalles', lazy=True))

class SalidasDeBano(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('salidas_de_bano', lazy=True))

class Cojuntos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('cojuntos', lazy=True))

class Bolsos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('bolsos', lazy=True))

# Lista de categorías
categories = ['Vestidos de baño', 'Crop tops', 'Amigurumis', 'Detalles', 'Salidas de baño', 'Cojuntos', 'Bolsos']

@app.route('/create_product', methods=['GET', 'POST'])
def create_product():
    new_product = None  # Inicializa new_product fuera del bloque condicional

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = float(request.form['price'])
        category = request.form['category']

        selected_category = Category.query.filter_by(name=category).first()

        if selected_category is None:
            return render_template('create_product.html', categories=categories, error_message='Categoría no válida')

        # Dependiendo de la categoría seleccionada, creamos el objeto correspondiente
        if category == 'Vestidos de baño':
            new_product = VestidosDeBano(title=title, description=description, price=price, category=selected_category)
        elif category == 'Crop tops':
            new_product = CropTops(title=title, description=description, price=price, category=selected_category)
        elif category == 'Amigurumis':
            new_product = Amigurumis(title=title, description=description, price=price, category=selected_category)
        elif category == 'Detalles':
            new_product = Detalles(title=title, description=description, price=price, category=selected_category)
        elif category == 'Salidas de baño':
            new_product = SalidasDeBano(title=title, description=description, price=price, category=selected_category)
        elif category == 'Cojuntos':
            new_product = Cojuntos(title=title, description=description, price=price, category=selected_category)
        elif category == 'Bolsos':
            new_product = Bolsos(title=title, description=description, price=price, category=selected_category)

        # Manejo de la imagen después de guardar el producto
        if new_product is not None:
            db.session.add(new_product)  # Añade el producto primero
            db.session.commit()  # Guarda el producto en la base de datos antes de manejar la imagen

            if 'photo' in request.files:
                photo = request.files['photo']
                if photo.filename != '':
                    _, extension = os.path.splitext(photo.filename)
                    filename = f"{new_product.id}{extension}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    photo.save(filepath)

                    # Convierte la imagen a base64
                    with open(filepath, "rb") as image_file:
                        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

                    # Guarda la representación base64 en la base de datos
                    new_product.image = encoded_image
                    db.session.commit()  # Realiza el commit nuevamente para guardar la imagen

            #return redirect(url_for('productos'))

    return render_template('create_product.html', categories=categories)

@app.route('/edit_product/<string:categoria>/<int:product_id>', methods=['GET', 'POST'])
def edit_product(categoria, product_id):
    product_class = globals()[categoria.replace(' ', '')]
    product = product_class.query.get_or_404(product_id)

    if request.method == 'POST':
        product.title = request.form['title']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.category_id = int(request.form['category'])

        db.session.commit()

        return redirect(url_for('home'))

    categories = Category.query.all()

    return render_template('edit_product.html', product=product, categories=categories)

@app.route('/delete_product/<string:categoria>/<int:product_id>')
def delete_product(categoria, product_id):
    product_class = globals()[categoria.replace(' ', '')]
    product = product_class.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/')
def home():
    categories = Category.query.all()
    # Obtén todos los productos a través de las relaciones con las categorías
    products = []
    for category in categories:
        products.extend(getattr(category, 'vestidos_de_bano', []))
        products.extend(getattr(category, 'crop_tops', []))
        products.extend(getattr(category, 'amigurumis', []))
        products.extend(getattr(category, 'detalles', []))
        products.extend(getattr(category, 'salidas_de_bano', []))
        products.extend(getattr(category, 'cojuntos', []))
        products.extend(getattr(category, 'bolsos', []))
    return render_template('home.html', products=products)

@app.route('/productos')
def productos():
    categories = Category.query.all()
    products = []
    for category in categories:
        # Obtén los productos de la categoría directamente desde la relación definida en el modelo
        products.extend(category.vestidos_de_bano)  
        products.extend(category.crop_tops)
        products.extend(category.amigurumis)
        products.extend(category.detalles)
        products.extend(category.salidas_de_bano)
        products.extend(category.cojuntos)
        products.extend(category.bolsos)
    return render_template('productos.html', products=products, categories=categories)

@app.route('/productos/<string:nombre_categoria>')
def categoria(nombre_categoria):
    # Busca la categoría en la base de datos
    category = Category.query.filter_by(name=nombre_categoria).first()
    print(f"DEBUG: Categoría encontrada: {category}")

    if not category:
        abort(404)

    # Obtén los productos de la categoría
    products = []
    products.extend(getattr(category, 'vestidos_de_bano', []))
    products.extend(getattr(category, 'crop_tops', []))
    products.extend(getattr(category, 'amigurumis', []))
    products.extend(getattr(category, 'detalles', []))
    products.extend(getattr(category, 'salidas_de_bano', []))
    products.extend(getattr(category, 'cojuntos', []))
    products.extend(getattr(category, 'bolsos', []))

    # Imprime información para depuración
    print(f"DEBUG: Nombre de la categoría: {nombre_categoria}")
    print(f"DEBUG: Productos de la categoría: {products}")

    return render_template('productos.html', products=products, nombre_categoria=nombre_categoria)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

with app.app_context():
    db.create_all()
    print("Tablas creadas con éxito")

def insert_categories():
    # Lista de categorías que deseas asegurarte de que existan
    categories_to_insert = ['Vestidos de baño', 'Crop tops', 'Amigurumis', 'Detalles', 'Salidas de baño', 'Cojuntos', 'Bolsos']

    # Recorre la lista de categorías y verifica/inserción en la base de datos
    with app.app_context():
        for category_name in categories_to_insert:
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                # La categoría no existe, así que la insertamos
                category = Category(name=category_name)
                db.session.add(category)
                db.session.commit()

# Ejecuta la función dentro del contexto de la aplicación
insert_categories()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
    print(app.url_map)
