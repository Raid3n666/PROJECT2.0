import sqlite3

con = sqlite3.connect('db/metalHeaders.db', check_same_thread= False)

cur = con.cursor()

class DAL:

    def __init__(self):
        cur.execute('CREATE TABLE IF NOT EXISTS bands (id TEXT PRIMARY KEY, name TEXT, img TEXT)') # ADDED IMAGE
        cur.execute('CREATE TABLE IF NOT EXISTS venues (id TEXT PRIMARY KEY, name TEXT, city TEXT)')
        cur.execute('CREATE TABLE IF NOT EXISTS shows (id TEXT PRIMARY KEY, bands TEXT, venue TEXT, date TEXT, time TEXT, price INT)') ## ADDED PRICE+BAND CHANGED TO BANDS
        cur.execute('CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, type INT, email TEXT, username TEXT, password TEXT)')
        cur.execute('CREATE TABLE IF NOT EXISTS updates (user id TEXT, band id TEXT, email TEXT, status INT)')
        cur.execute('CREATE TABLE IF NOT EXISTS comments (user id TEXT, show id, content TEXT)')

    def venue_objects(self):
        objects = []
        cur.execute('SELECT * FROM venues')
        res = cur.fetchall()
        res = list(res)
        for venue in res:
            venue = Venue(venue[1], venue[2], venue[0])
            objects.append(venue)
        return objects
    
    def band_objects(self):
        objects = []
        cur.execute('SELECT * FROM bands')
        res = cur.fetchall()
        res = list(res)
        for band in res:
            band = Band(band[1], band[0], band[2])
            objects.append(band)
        return objects
    
    def show_objects(self):
        objects = []
        cur.execute('SELECT * FROM shows')
        res = cur.fetchall()
        res = list(res)
        for show in res:
            show = Show(show[0], show[1], show[2], show[3], show[4], show[5])
            objects.append(show)
        return objects

class Band:

    def __init__(self, name = None, id = None, img = None) -> None:
        self.name = name
        self.id = id
        self.img = img

    def all_bands(self):
        cur.execute('SELECT name FROM bands')
        all = cur.fetchall()
        bands = []
        for i in all:
            i = str(i)
            i = i.strip("(',')")
            bands.append(i)
        return bands

    def add(self):
        if self.name not in self.all_bands() and self.name != '':
            cur.execute(f'INSERT INTO bands VALUES ("{self.id}", "{self.name}", "{self.img}")')
            con.commit()
            return True
        else:
            return False

    def remove(self):
        try:
            cur.execute(f'SELECT id FROM bands WHERE name = "{self.name}"')
            self.id = cur.fetchone()[0]
            cur.execute(f'DELETE FROM bands WHERE id = "{self.id}"')
            con.commit()
            return True
        except:
            return False
    
    def get_by_id(self):
        try:
            cur.execute(f'SELECT * FROM bands WHERE id = "{self.id}"')
            res = cur.fetchone()
            band = Band(res[1], res[0], res[2])
            return band
        except:
            return False

class Venue:

    def __init__(self, name, city, id = None) -> None:
        self.name = name
        self. city = city
        self.id = id

    def add(self):
        if (self.name, self.city) not in self.all_venues() and self.name != '':
            cur.execute(f'INSERT INTO venues VALUES ("{self.id}", "{self.name}", "{self.city}")')
            con.commit()
            return True
        else:
            return False

    def remove(self):
        try:
            cur.execute(f'SELECT id FROM venues WHERE name = "{self.name}" AND city = "{self.city}"')
            self.id = cur.fetchone()[0]
            cur.execute(f'DELETE FROM venues WHERE id = "{self.id}"')
            con.commit()
            return True
        except:
            return False
    
    def all_venues(self):
        cur.execute('SELECT name, city FROM venues')
        res = cur.fetchall()
        venues = []
        for i in res:
            venues.append(i)
        return venues

class Show:

    def __init__(self, id, band, venue, date, time, price) -> None:
        self.id = id
        self.band = band
        self.venue = venue
        self.date = date
        self.time = time
        self.price = price
    
    def all_shows(self):
        cur.execute('SELECT bands, venue, date, time, price FROM shows')
        res = cur.fetchall()
        shows = list(res)
        return shows
    
    def add(self):
        if (self.band, self.venue, self.date) not in self.all_shows():
            cur.execute(f'INSERT INTO shows VALUES ("{self.id}", "{self.band}", "{self.venue}", "{self.date}", "{self.time}", {self.price})')
            con.commit()
            return True
        else:
            return False
    
    def remove(self):
        try:
            cur.execute(f'DELETE FROM shows WHERE id = "{self.id}"')
            con.commit()
            return True
        except:
            return False
    
    def get_by_id(self):
        try:
            cur.execute(f'SELECT * FROM shows WHERE id = "{self.id}"')
            res = cur.fetchone()
            show = Show(self.id, res[1], res[2], res[3], res[4], res[5])
            return show
        except:
            return False
    
    def edit(self, new_band, new_venue, new_date, new_time, new_price):
        if (new_band, new_venue, new_date, new_time, new_price) not in self.all_shows():
            cur.execute(f'UPDATE shows SET bands = "{new_band}", venue = "{new_venue}", date = "{new_date}", time = "{new_time}", price = {new_price} WHERE id = "{self.id}"')
            con.commit()
            return True
        else:
            return False

