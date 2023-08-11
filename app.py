from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from forms import AddPetForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pets'

# Initialize the database instance
db = SQLAlchemy(app)

# Set up the Debug Toolbar
toolbar = DebugToolbarExtension(app)

# Import the Pet model (add more imports if needed for other models)
from models import Pet

# Create the tables before running the app
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    pets = Pet.query.all()
    return render_template('index.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    form = AddPetForm()

    if form.validate_on_submit():
        try:
            # Create a new pet from the form data and add it to the database
            new_pet = Pet(
                name=form.name.data,
                species=form.species.data,
                photo_url=form.photo_url.data,
                age=form.age.data,
                notes=form.notes.data,
                available=form.available.data
            )
            db.session.add(new_pet)
            print("Adding pet:", form.name.data, form.species.data, form.age.data)
            db.session.commit()

            # Redirect to the homepage after adding a pet
            return redirect(url_for('index'))
        except Exception as e:
            # Handle the exception (print, log, or display an error message)
            print("Error:", e)

    return render_template('add_pet.html', form=form)

@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def view_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if pet is None:
        return "Pet not found", 404

    form = AddPetForm(obj=pet)

    if form.validate_on_submit():
        # Update the pet data based on the form input
        form.populate_obj(pet)
        db.session.commit()
        return redirect(url_for('view_pet', pet_id=pet.id))

    return render_template('view_pet.html', pet=pet, form=form)

if __name__ == '__main__':
    app.run(debug=True)