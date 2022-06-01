from flask import Flask, redirect, render_template, url_for, request
# from flask import Flask, redirect, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField
import folium
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Points(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.String(200))
    lon = db.Column(db.String(200))
    bache_name = db.Column(db.String(200))

    def __init__(self, lat, lon, bache_name):
        self.lat = lat
        self.lon = lon
        self.bache_name = bache_name

    def __repr__(self) -> str:
        return f'<Hola: {self.bache_name}>'


class CargarForm(FlaskForm):
    dynamic_select = StringField("Choose an option")


@app.route("/")
def base():
    # this is base map
    map = folium.Map(
        location=[-25.302058396540463, -57.58112871603071],
        zoom_start=13,
        # width=550,
        # height=350
        # folium_map = folium.Map(location=[-25.30216509196748   , -57.58115017370211], zoom_start=20)
    )
    points = Points.query.all()
    listita = []
    for point in points:
        listita.append([point.lat, point.lon])
        print(listita)
    # lista = [[-25.302058396540463, -56.58112871603071], [-25.302458396540463, -55.58122871603071], [-25.3035769, -57.5833092]]

    for x in listita:
        mark = x[0],x[1]
        print(x)
        # # print(i)
        folium.Marker(
    

            location=i,
            popup="<b>point.bache_name</b>",
            tooltip="bache!"
        ).add_to(map)
    return map._repr_html_()


@app.route("/crear-bache", methods = ['POST', 'GET'])
def crearbache():
    form = CargarForm()


    if request.method == 'POST':
        point = Points(
            lat=request.form['lat'],
            lon=request.form['lon'],
            bache_name = request.form['bache_name']
        )
        db.session.add(point)
        db.session.commit()
        return redirect(url_for('base'))
    else:
        return render_template('crear-bache.html', form = form)


@app.route("/open-street-map")
def open_street_map():
    lista = [[-25.302058396540463, -56.58112871603071], [-25.302458396540463, -55.58122871603071]]


    # this map using stamen toner
    map = folium.Map(
        location=[45.52336, -122.6750],
        tiles='Stamen Toner',
        zoom_start=13
    )

    for i in lista:
        print(i) 
        # for x in i:
        folium.Marker(
    

            location=i,
            popup="<b>Marker here</b>",
            tooltip="Click Here!"
        ).add_to(map)
        
    
    return map._repr_html_()

@app.route("/map-marker")
def map_marker():
    # this map using stamen terrain
    # we add some marker here
    map = folium.Map(
        location=[45.52336, -122.6750],
        tiles='Stamen Terrain',
        zoom_start=12
    )

    folium.Marker(
        location=[45.52336, -122.6750],
        popup="<b>Marker here</b>",
        tooltip="Click Here!"
    ).add_to(map)

    folium.Marker(
        location=[45.55736, -122.8750],
        popup="<b>Marker 2 here</b>",
        tooltip="Click Here!",
        icon=folium.Icon(color='green')
    ).add_to(map)

    folium.Marker(
        location=[45.53236, -122.8750],
        popup="<b>Marker 3 here</b>",
        tooltip="Click Here!",
        icon=folium.Icon(color='red')
    ).add_to(map)

    return map._repr_html_()

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)