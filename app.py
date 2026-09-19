import os
from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from config import Config
from models import db, User, Property, Wishlist
from forms import RegistrationForm, LoginForm, PropertyForm, SearchForm, ContactForm, UpdateProfileForm, ChangePasswordForm, ForgotPasswordForm, ResetPasswordForm
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

db.init_app(app)

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def create_tables():
    with app.app_context():
        db.create_all()

# ensure database exists on startup
create_tables()


@app.context_processor
def inject_current_year():
    return {'current_year': datetime.utcnow().year}

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    props = Property.query.order_by(Property.created_at.desc()).paginate(page=page, per_page=6)
    return render_template('index.html', properties=props)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter((User.email==form.email.data)|(User.username==form.username.data)).first():
            flash('Email or username already registered', 'danger')
            return redirect(url_for('register'))
        user = User(username=form.username.data, email=form.email.data, name=form.name.data, phone=form.phone.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    page = request.args.get('page', 1, type=int)
    props = Property.query.filter_by(user_id=current_user.id).order_by(Property.created_at.desc()).paginate(page=page, per_page=6)
    return render_template('dashboard.html', properties=props)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Profile updated', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html', form=form)

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Old password is incorrect', 'danger')
            return redirect(url_for('change_password'))
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Password changed', 'success')
        return redirect(url_for('profile'))
    return render_template('change_password.html', form=form)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = serializer.dumps(user.email, salt='password-reset-salt')
            reset_url = url_for('reset_password', token=token, _external=True)
            flash(f'Password reset link: {reset_url}', 'info')
        else:
            flash('If that email exists, a reset link was generated.', 'info')
        return redirect(url_for('login'))
    return render_template('forgot_password.html', form=form)

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except Exception:
        flash('The reset link is invalid or expired.', 'danger')
        return redirect(url_for('forgot_password'))
    user = User.query.filter_by(email=email).first_or_404()
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        db.session.commit()
        flash('Password has been reset. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/property/add', methods=['GET', 'POST'])
@login_required
def add_property():
    form = PropertyForm()
    if form.validate_on_submit():
        prop = Property(
            title=form.title.data,
            description=form.description.data,
            purpose=form.purpose.data,
            property_type=form.property_type.data,
            price=float(form.price.data) if form.price.data else 0,
            deposit=float(form.deposit.data) if form.deposit.data else 0,
            bedrooms=form.bedrooms.data,
            bathrooms=form.bathrooms.data,
            balcony=form.balcony.data,
            parking=form.parking.data,
            area_size=form.area_size.data,
            floor=form.floor.data,
            facing=form.facing.data,
            furnished=form.furnished.data,
            water=form.water.data,
            electricity=form.electricity.data,
            internet=form.internet.data,
            address=form.address.data,
            locality=form.locality.data,
            city=form.city.data,
            district=form.district.data,
            state=form.state.data,
            pincode=form.pincode.data,
            google_map=form.google_map.data,
            owner_name=form.owner_name.data,
            owner_phone=form.owner_phone.data,
            owner_email=form.owner_email.data,
            available_from=form.available_from.data,
            user_id=current_user.id
        )
        image_filenames = []
        images = request.files.getlist('images')
        for image in images:
            if image and allowed_file(image.filename):
                filename = secure_filename(f"{datetime.utcnow().timestamp()}_{image.filename}")
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(path)
                image_filenames.append(filename)
        prop.images = ','.join(image_filenames)
        db.session.add(prop)
        db.session.commit()
        flash('Property added successfully', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_property.html', form=form)

@app.route('/property/<int:property_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_property(property_id):
    prop = Property.query.get_or_404(property_id)
    if prop.user_id != current_user.id:
        abort(403)
    form = PropertyForm(obj=prop)
    if form.validate_on_submit():
        existing_images = prop.images if prop.images else ''
        form.populate_obj(prop)
        if isinstance(prop.images, list):
            prop.images = existing_images
        image_filenames = []
        if prop.images:
            if isinstance(prop.images, str):
                image_filenames = [f for f in prop.images.split(',') if f]
            elif isinstance(prop.images, list):
                image_filenames = [f for f in prop.images if f]
        images = request.files.getlist('images')
        for image in images:
            if image and allowed_file(image.filename):
                filename = secure_filename(f"{datetime.utcnow().timestamp()}_{image.filename}")
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(path)
                image_filenames.append(filename)
        prop.images = ','.join([f for f in image_filenames if f])
        db.session.commit()
        flash('Property updated', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_property.html', form=form, property=prop)

@app.route('/property/<int:property_id>/delete', methods=['POST'])
@login_required
def delete_property(property_id):
    prop = Property.query.get_or_404(property_id)
    if prop.user_id != current_user.id:
        abort(403)
    # delete images
    if prop.images:
        for fname in prop.images.split(','):
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            except Exception:
                pass
    db.session.delete(prop)
    db.session.commit()
    flash('Property deleted', 'success')
    return redirect(url_for('dashboard'))

@app.route('/properties')
def properties():
    page = request.args.get('page', 1, type=int)
    form = SearchForm(request.args)
    query = Property.query
    if form.keyword.data:
        query = query.filter(Property.title.ilike(f"%{form.keyword.data}%"))
    if form.city.data:
        query = query.filter(Property.city.ilike(f"%{form.city.data}%"))
    if form.min_price.data:
        query = query.filter(Property.price >= float(form.min_price.data))
    if form.max_price.data:
        query = query.filter(Property.price <= float(form.max_price.data))
    props = query.order_by(Property.created_at.desc()).paginate(page=page, per_page=8)
    return render_template('properties.html', properties=props, form=form)

@app.route('/property/<int:property_id>')
def property_details(property_id):
    prop = Property.query.get_or_404(property_id)
    images = prop.images.split(',') if prop.images else []
    return render_template('property_details.html', property=prop, images=images)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/wishlist/add/<int:property_id>', methods=['POST'])
@login_required
def add_wishlist(property_id):
    if Wishlist.query.filter_by(user_id=current_user.id, property_id=property_id).first():
        flash('Already in wishlist', 'info')
    else:
        w = Wishlist(user_id=current_user.id, property_id=property_id)
        db.session.add(w)
        db.session.commit()
        flash('Added to wishlist', 'success')
    return redirect(request.referrer or url_for('properties'))

@app.route('/wishlist')
@login_required
def wishlist():
    page = request.args.get('page', 1, type=int)
    items = Wishlist.query.filter_by(user_id=current_user.id).join(Property).paginate(page=page, per_page=8)
    return render_template('wishlist.html', items=items)

@app.route('/wishlist/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_wishlist(item_id):
    item = Wishlist.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Removed from wishlist', 'success')
    return redirect(url_for('wishlist'))

@app.route('/contact/<int:property_id>', methods=['GET', 'POST'])
def contact_owner(property_id):
    prop = Property.query.get_or_404(property_id)
    form = ContactForm()
    if form.validate_on_submit():
        # In production: send email to owner. For now flash a message.
        flash('Message sent to property owner (simulated).', 'success')
        return redirect(url_for('property_details', property_id=property_id))
    return render_template('contact.html', form=form, property=prop)

@app.route('/search')
def search():
    return redirect(url_for('properties'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash('Message received. We will contact you soon.', 'success')
        return redirect(url_for('index'))
    return render_template('contact.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
