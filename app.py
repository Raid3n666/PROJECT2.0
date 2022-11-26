from flask import Flask, render_template, request, flash, url_for, redirect
from modules.cities import cities
import os
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_user, logout_user, login_required, current_user, LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = '666'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/metalHeaders.db'
app.config['UPLOAD_FOLDER'] = 'static/images'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'guest'

db = SQLAlchemy(app, session_options = {'autoflush' : False})

bcrypt = Bcrypt(app)

api = Api(app)

CORS(app)

### MODELS ####
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(15), unique = True, nullable = False)
    password = db.Column(db.String(15), nullable = False)
    email = db.Column(db.String(20), nullable = False, unique = True)
    profile_pic = db.Column(db.String(300))


class Shows(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    band = db.Column(db.String(20), nullable = False)
    venue = db.Column(db.String(30), nullable = False)
    date = db.Column(db.DateTime)
    time = db.Column(db.DateTime)
    price = db.Column(db.Integer)
    likes = db.Column(db.Integer, default = 0)
    img = db.Column(db.String(30))
    description = db.Column(db.String(300))

    def serialize(self):
        return {
            'id' : self.id,
            'band' : self.band,
            'venue' : self.venue,
            'date' : self.date.strftime('%d/%m/%Y'),
            'time' : self.time.strftime('%H:%M'),
            'price' : self.price,
            'likes' : self.likes,
            'img' : self.img
        }

class Bands(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    img = db.Column(db.String(30))

    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'img' : self.img
        }

class Venues(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    city = db.Column(db.String(20), nullable = False)
    
class Likes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable = False)
    show_id = db.Column(db.Integer, nullable = False)

    def serialize(self):
        return {
            'id' : self.id,
            'user_id' : self.user_id,
            'show_id' : self.show_id
        }

class Stars(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable = False)
    show_id = db.Column(db.Integer, nullable = False)

    def serialize(self):
        return {
            'id' : self.id,
            'user_id' : self.user_id,
            'show_id' : self.show_id
        }

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable = False)
    username = db.Column(db.String(15), nullable = False)
    profile_picture = db.Column(db.String)
    show_id = db.Column(db.Integer, nullable = False)
    content = db.Column(db.String(300), nullable = False)
    likes = db.Column(db.Integer, default = 0, nullable = False)
    date = db.Column(db.DateTime, default = datetime.now)

    def serialize(self):
        return {
            'id' : self.id,
            'user_id' : self.user_id,
            'show_id' : self.show_id,
            'content' : self.content
        }

class CommentsLikes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable = False)
    comment_id = db.Column(db.Integer, nullable = False)


##### ADMIN APP #####
@app.route('/', methods = ['POST', 'GET'])
@login_required
def index():
    if current_user.id != 1:
        return redirect(url_for('website'))
    bands = Bands().query.all()
    venues = Venues().query.all()
    if request.method == 'GET':
        shows = Shows().query.all()
        amount = len(shows)
        return render_template('shows.html', bands = bands, venues = venues, shows = shows, amount = amount)
    else:
        try:
            shows = Shows.query.all()
            band = request.form['band']
            venue = request.form['venue']
            date = datetime.strptime(request.form['date'], '%Y-%m-%d')
            time = datetime.strptime(request.form['time'], '%H:%M')
            price = request.form['price']
            band_object = Bands.query.filter_by(name = band).first()
            img = band_object.img
            description = request.form['description']
            for show in shows:
                if show.band == band and show.venue == venue and show.date == date:
                    flash('Show exists')
                    return redirect(url_for('index'))
            show = Shows(band = band, venue = venue, date = date, time = time, price = price, img = img, description = description)
            db.session.add(show)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            flash('FILL ALL FIELDS')
            return redirect(url_for('index'))

@app.route('/users')
@login_required
def users():
    if current_user.id != 1:
        return redirect(url_for('website'))
    users = Users.query.all()
    amount = len(users)
    return render_template('users.html', users = users, amount = amount)

@app.route('/users/remove_user/<int:id>')
@login_required
def remove_user(id):
    if current_user.id != 1:
        return redirect(url_for('website'))
    user = Users.query.get(id)
    db.session.delete(user)
    db.session.commit()
    flash('User removed')
    return redirect(url_for('users'))

@app.route('/bands', methods = ['POST', 'GET'])
@login_required
def bands():
    if current_user.id != 1:
        return redirect(url_for('website'))
    if request.method == 'GET':
        bands = Bands().query.all()
        amount = len(bands)
        return render_template('bands.html', bands = bands, amount = amount)
    else:
        name = request.form['band']
        list_of_bands = [band.name for band in Bands.query.all()]
        if name in list_of_bands:
            flash('Band name exists')
            return redirect(url_for('bands'))
        image = request.files['image']
        if image.filename != '':
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
        else:
            image.filename = None
        band = Bands(name = name, img = image.filename)
        db.session.add(band)
        db.session.commit()
        bands = Bands().query.all()
        amount = len(bands)
        return render_template('bands.html', bands = bands, amount = amount)

@app.route('/venues', methods = ['POST','GET'])
@login_required
def venues():
    if current_user.id != 1:
        return redirect(url_for('website'))
    if request.method == 'GET':
        venues = Venues().query.all()
        amount = len(venues)
        return render_template('venues.html', cities = cities, venues = venues, amount = amount)
    else:
        name = request.form['name']
        city = request.form['city']
        venues = Venues.query.all()
        for venue in venues:
            if venue.name == name and venue.city == city:
                flash('Venue exists')
                return redirect(url_for('venues'))
        venue = Venues(name = name, city = city)
        db.session.add(venue)
        db.session.commit()
        venues = Venues().query.all()
        amount = len(venues)
        return render_template('venues.html', cities = cities, venues = venues, amount = amount)


#### REMOVES ####
@app.route('/bands/remove=<id>')
@login_required
def remove_band(id):
    if current_user.id != 1:
        return redirect(url_for('website'))
    band = Bands.query.get(id)
    db.session.delete(band)
    db.session.commit()
    flash('Band removed')
    return redirect(url_for('bands'))

@app.route('/venues/remove=<id>')
@login_required
def remove_venue(id):
    if current_user.id != 1:
        return redirect(url_for('website'))
    venue = Venues.query.get(id)
    db.session.delete(venue)
    db.session.commit()
    flash('Venue removed')
    return redirect(url_for('venues'))

@app.route('/remove=<id>')
@login_required
def remove_show(id):
    if current_user.id != 1:    
        return redirect(url_for('website'))
    show = Shows.query.get(id)
    db.session.delete(show)
    db.session.commit()
    flash('Show removed')
    return redirect(url_for('index'))

### EDIT ###
@app.route('/edit=<showid>', methods = ['POST', 'GET'])
@login_required
def edit_show(showid):
    if current_user.id != 1:
        return redirect(url_for('website'))
    show_obj = Shows.query.get(showid)
    if request.method == 'GET':
        bands = Bands.query.all()
        venues = Venues.query.all() 
        show_obj.venue = show_obj.venue.strip().split('-')[0].strip()
        show_obj.date = str(show_obj.date)[:10]
        show_obj.time = str(show_obj.time.time())
        return render_template('edit.html', bands = bands, venues = venues, show = show_obj)
    else:
        band = request.form['band']
        venue = request.form['venue']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        time = datetime.strptime(request.form['time'][:5], '%H:%M')
        price = request.form['price']
        description = request.form['description']
        show_obj.band = band
        show_obj.venue = venue
        show_obj.date = date
        show_obj.time = time
        show_obj.price = price
        show_obj.description = description
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/add_image/<int:band_id>', methods = ['POST', 'GET'])
@login_required
def add_image(band_id):
    if current_user.id != 1:
        return redirect(url_for('website'))
    band = Bands.query.get(band_id)
    if request.method == 'POST':
        file = request.files['image']
        if band.img == None:
            band.img = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            flash('Image added')
        else:
            try:
                os.remove(f'{app.config["UPLOAD_FOLDER"]}/{band.img}')
            except:
                pass
            band.img = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            shows = Shows.query.filter_by(band = band.name)
            for show in shows:
                show.img = band.img
            flash('Image Updated')
        db.session.commit()
        return redirect(url_for('bands'))
    return render_template('add_image.html')        
  
###################### WEBSITE #############################
@app.route('/website/')
@login_required
def website():
    shows = Shows.query.order_by(Shows.date)
    user_id = current_user.id
    likes = [like.show_id for like in Likes.query.filter_by(user_id = user_id)]
    stars = [star.show_id for star in Stars.query.filter_by(user_id = user_id)]
    return render_template('website/index.html', shows = shows, current_user = current_user, likes = likes, stars = stars)

@app.route('/website/show/<int:show_id>', methods = ['POST', 'GET'])
@login_required
def show(show_id):
    show = Shows.query.get(show_id)
    user_id = current_user.id
    likes = [like.show_id for like in Likes.query.filter_by(user_id = user_id)]
    stars = [star.show_id for star in Stars.query.filter_by(user_id = user_id)]
    comments = [comment for comment in Comments.query.filter_by(show_id = show.id)]
    comment_likes = [comment.comment_id for comment in CommentsLikes.query.filter_by(user_id = user_id)]
    if request.method == 'POST':
        comment_content = request.form['comment']
        comment = Comments()
        comment.username = current_user.username
        comment.profile_picture = current_user.profile_pic
        comment.user_id = user_id
        comment.show_id = show.id
        comment.content = comment_content
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('show', show_id = show.id))
    comments.sort(key = lambda comment: comment.date, reverse = True)
    for comment in comments:
        comment.date = comment.date.strftime("%d/%m/%Y %H:%M")
    return render_template('/website/show.html', show = show, current_user = current_user, likes = likes, stars = stars, comments = comments, comment_likes = comment_likes)

@app.route('/website/search')
@login_required
def website_search():
    bands = Bands.query.all()
    user_id = current_user.id
    results = []
    search_word = request.args.get('band')
    for band in bands:
        print(band.name.lower())
        if search_word.lower() in band.name.lower():
            results.append(band.name)
    shows = [show for show in Shows.query.all() if show.band in results]
    likes = [like.show_id for like in Likes.query.filter_by(user_id = user_id)]
    stars = [star.show_id for star in Stars.query.filter_by(user_id = user_id)]
    if len(shows) == 0:
        flash('No results found, try a different keyword')
        return redirect(url_for('website'))
    return render_template('website/index.html', shows = shows, current_user = current_user, likes = likes, stars = stars)

@app.route('/website/guest')
def guest():
    shows = Shows.query.order_by(Shows.date)
    return render_template('/website/guest.html', shows = shows)

@app.route('/website/profile')
@login_required
def profile():
        starred_show_ids = [star.show_id for star in Stars.query.filter_by(user_id = current_user.id)]
        shows = [show for show in Shows.query.all() if show.id in starred_show_ids]
        return render_template('/website/profile.html', shows = shows, user = current_user)

######################### LOGIN & USERS ##################################
@app.route('/redirect_guest')
def redirect_guest():
    flash('You must login to like and star shows.')
    return redirect(url_for('login'))

@app.route('/redirect_guest2')
def redirect_guest_():
    flash('You must login to view show details.')
    return redirect(url_for('login'))

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 
        user = Users.query.filter_by(username = username).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('website'))
            else:
                flash('Wrong password')
        else:
            flash('User does not exist')
        return redirect(url_for('login'))
    return render_template('/website/login.html')

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

@app.route('/logout', methods = ['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('guest'))

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        usernames = [user.username for user in Users.query.all()]
        emails = [user.email for user in Users.query.all()]
        entered_username = request.form['username']
        entered_email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password)
        if len(entered_username) < 6 or entered_username.isdigit():
            flash('Username must conatin 6 or more letters and must not contain only numbers')
            return redirect(url_for('register'))
        for email in emails:
            if entered_email == email:
                flash('Email exists')
                return redirect(url_for('register'))
        for username in usernames:
            if entered_username == username:
                flash('Username exists')
                return redirect(url_for('register'))
        if password.isdigit():
            flash('Password must contain letters')
            return redirect(url_for('register'))
        image = request.files['profile_picture']
        user = Users()
        user.username = entered_username
        user.email = entered_email
        user.password = hashed_password
        if image.filename != '':
            user.profile_pic = image.filename
            image.save(os.path.join(f"{app.config['UPLOAD_FOLDER']}\\profile_pictures", image.filename))
        else:
            user.profile_pic = 'default.png'
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully')
        return redirect(url_for('login'))
    return render_template('/website/register.html')

@app.route('/change_password/<int:user_id>', methods = ['POST'])
@login_required
def change_password(user_id):
    user = Users.query.get(user_id)
    entered_password = request.form['password']
    if entered_password.isdigit():
        flash('Password must cotain letters')
        return redirect(url_for('profile'))
    new_password = bcrypt.generate_password_hash(entered_password)
    user.password = new_password
    db.session.commit()
    flash('Password changed')
    return redirect(url_for('profile'))

@app.route('/change_profile_pic/<int:user_id>', methods = ['POST'])
@login_required
def change_profile_pic(user_id):
    user = Users.query.get(user_id)
    image = request.files['profile_pic']
    if user.profile_pic == 'default.png':
        user.profile_pic = image.filename
        image.save(os.path.join(f"{app.config['UPLOAD_FOLDER']}\\profile_pictures", image.filename))
    else:
        try:
            os.remove(f'{app.config["UPLOAD_FOLDER"]}//profile_pictures//{user.profile_pic}')
        except:
            pass
        user.profile_pic = image.filename
        image.save(os.path.join(f"{app.config['UPLOAD_FOLDER']}\\profile_pictures", image.filename))
    comments = Comments.query.filter_by(user_id = user_id)
    for comment in comments:
        comment.profile_picture = user.profile_pic
    db.session.commit()
    flash('New profile picture set successfully')
    return redirect(url_for('profile'))


########## API ############

class Allshows(Resource):
    def get(self):
        shows = Shows().query.all()
        return [show.serialize() for show in shows]

class Allbands(Resource):
    def get(self):
        bands = Bands().query.all()
        return [band.serialize() for band in bands]

class AddLikes(Resource):

    def post(self, show_id):
        like = Likes()
        data = request.get_json()
        like.show_id = show_id
        like.user_id = data['user_id']
        show_to_like = Shows.query.get(int(like.show_id))
        likes = [(like.show_id, like.user_id) for like in Likes.query.all()]
        if (like.show_id, like.user_id) in likes:
            show_to_like.likes -= 1
            print('hi')
            like_to_delete = Likes.query.filter_by(user_id = like.user_id, show_id = like.show_id)[0]
            db.session.delete(like_to_delete)
            db.session.commit()
        else:
            show_to_like.likes += 1
            db.session.add(like)
            db.session.commit()
        return like.serialize()
    
class AllLikes(Resource):
    
    def get(self):
        likes = Likes().query.all()
        return [like.serialize() for like in likes]

class AddStars(Resource):

    def post(self, show_id):
        star = Stars()
        data = request.get_json()
        star.show_id = show_id
        star.user_id = data['user_id']
        stars = [(star.show_id, star.user_id) for star in Stars.query.all()]
        if (star.show_id, star.user_id) in stars:
            star_to_delete = Stars.query.filter_by(user_id = star.user_id, show_id = star.show_id)[0]
            db.session.delete(star_to_delete)
            db.session.commit()
        else:
            db.session.add(star)
            db.session.commit()
        return star.serialize()
    
class AllStars(Resource):
    
    def get(self):
        stars = stars().query.all()
        return [star.serialize() for star in stars]

class Comment(Resource):

    def post(self, show_id):
        data = request.get_json()
        comment = Comments()
        user_id = data['user_id']
        content = data['content']
        comment.show_id = show_id
        comment.user_id = user_id
        comment.content = content
        db.session.add(comment)
        db.session.commit()
        return comment.serialize()    

    def get(self, show_id):
        comments = Comments.query.all()
        related_comments = []
        for comment in comments:
            if comment.show_id == show_id:
                related_comments.append(comment)
        return [comment.serialize() for comment in related_comments]

class LikeComment(Resource):

    def post(self, comment_id):
        data = request.get_json()
        comment = Comments.query.get(comment_id)
        likes = [(like.comment_id, like.user_id) for like in CommentsLikes.query.all()]
        if (comment_id, data['user_id']) in likes:
            comment.likes -= 1
            like_to_delete = CommentsLikes.query.filter_by(comment_id = comment_id, user_id = data['user_id'])[0]
            db.session.delete(like_to_delete)
            db.session.commit()
        else:
            comment.likes += 1
            like = CommentsLikes()
            like.user_id = data['user_id']
            like.comment_id = comment_id
            db.session.add(like)
            db.session.commit()

#######################################################
db.create_all()
api.add_resource(Allshows, '/api/shows')
api.add_resource(Allbands, '/api/bands')
api.add_resource(AddLikes, '/api/like/<int:show_id>')
api.add_resource(AllLikes, '/api/likes')
api.add_resource(AddStars, '/api/star/<int:show_id>')
api.add_resource(AllStars, '/api/stars')
api.add_resource(Comment, '/api/comment/<int:show_id>')
api.add_resource(LikeComment, '/api/likecomment/<int:comment_id>')

if __name__ == '__main__':

    app.run(debug= True, host= '0.0.0.0', port = int(os.environ.get('PORT', 5000)))