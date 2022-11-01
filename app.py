from flask import Flask, render_template, request, flash, url_for, redirect
from modules.cities import cities
from modules.id_maker import make_id
from db.dal import DAL, Band, Venue, Show
from modules.time import Date
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = '666'
app.config['UPLOAD_FOLDER'] = 'static/images'

dal = DAL()

@app.route('/', methods = ['POST', 'GET'])
def index():
    bands = dal.band_objects()
    venues = dal.venue_objects()
    if request.method == 'GET':
        shows = dal.show_objects()
        amount = len(shows)
        return render_template('shows.html', bands = bands, venues = venues, shows = shows, amount = amount)
    else:
        try:
            band = request.form['band']
            venue = request.form['venue']
            date = Date(request.form['date']).formatted_date
            time = request.form['time']
            price = request.form['price']
            if time == '' or date == '//':
                flash ('Please select valid time and date')
                return redirect(url_for('index'))
            id = f's{make_id()}'
            show = Show(id, band, venue, date, time, price)
            if show.add():
                msg = 'Show added'
            else:
                msg = 'Show exists'
            shows = dal.show_objects()
            amount = len(shows)
            flash(msg)
            return redirect(url_for('index'))
        except:
            flash('FILL ALL FIELDS')
            return redirect(url_for('index'))


@app.route('/users')
def users():
    return render_template('users.html')

@app.route('/bands', methods = ['POST', 'GET'])
def bands():
    if request.method == 'GET':
        bands = dal.band_objects()
        amount = len(bands)
        return render_template('bands.html', bands = bands, amount = amount)
    else:
        name = request.form['band']
        image = request.files['image']
        if name == '':
            flash('Please enter a valid band name')
            return redirect(url_for('bands'))
        id = f'b{make_id()}'
        if image.filename != '':
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
        else:
            image.filename = None
        band = Band(name, id, image.filename)
        if band.add():
            message = 'Band added'
        else:
            message = 'Band exists'
        bands = dal.band_objects()
        amount = len(bands)
        flash(message)
        return render_template('bands.html', bands = bands, amount = amount)

@app.route('/venues', methods = ['POST','GET'])
def venues():
    if request.method == 'GET':
        venues = dal.venue_objects()
        amount = len(venues)
        return render_template('venues.html', cities = cities, venues = venues, amount = amount)
    else:
        name = request.form['name']
        if name == '':
            flash('Pleas enter a valid venue name')
            return redirect(url_for('venues'))
        city = request.form['city']
        id = f'v{make_id()}'
        v = Venue(name, city, id)
        if v.add():
            msg = 'Venue added'
        else:
            msg = 'Venue exists'
        venues = dal.venue_objects()
        amount = len(venues)
        flash(msg)
        return render_template('venues.html', cities = cities, venues = venues, amount = amount)


#### REMOVES ####
@app.route('/bands/remove=<name>')
def remove_band(name):
    band = Band(name)
    band.remove()
    flash('Band removed')
    return redirect(url_for('bands'))

@app.route('/venues/remove=<namecity>')
def remove_venue(namecity):
    namecity = namecity.split('&')
    name = namecity[0]
    city = namecity[1]
    v = Venue(name, city)
    v.remove()
    flash('Venue removed')
    return redirect(url_for('venues'))

@app.route('/remove=<showid>')
def remove_show(showid):
    show_obj = Show(showid, None, None, None, None, None)
    show_obj.remove()
    flash('Show removed')
    return redirect(url_for('index'))

### EDIT ###
@app.route('/edit=<showid>', methods = ['POST', 'GET'])
def edit_show(showid):
    show_obj = Show(showid, None, None, None, None, None)
    show_obj = show_obj.get_by_id()
    if request.method == 'GET':
        bands = dal.band_objects()
        venues = dal.venue_objects() 
        show_obj.venue = show_obj.venue.strip().split('-')[0].strip()
        show_obj.date = Date(show_obj.date).undo_formatting
        return render_template('edit.html', bands = bands, venues = venues, show = show_obj)
    else:
        band = request.form['band']
        venue = request.form['venue']
        date = Date(request.form['date']).formatted_date
        time = request.form['time']
        price = request.form['price']
        if show_obj.edit(band, venue, date, time, price):
            msg = f'Show {show_obj.id} updated'
        else:
            msg = 'Show exists'
        flash(msg)
        return redirect(url_for('index'))
        
@app.route('/bands/add_image=<bandId>') ### TO - DO
def add_image(bandId):
    band = Band(id = bandId).get_by_id()
    return f'{band.name}'   


if __name__ == '__main__':
    app.run(debug= True, port= 80, host= '0.0.0.0')