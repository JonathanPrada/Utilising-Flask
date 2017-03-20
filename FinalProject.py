# Import Flask class from flask library
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


# all the imports an application uses get called name
app = Flask(__name__)
# required for flash messaging
app.secret_key = 'some_secret'


# connect to our database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    Menu_Item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(Menu_Item=Menu_Item.serialize)


@app.route('/restaurant/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants=[r.serialize for r in restaurants])


# url addresses for our main page
@app.route('/')
@app.route('/restaurant')
def restaurant():
    restaurants = session.query(Restaurant).all()
    #This will return a template that shows all the restaurants
    return render_template('restaurants.html', restaurants = restaurants)


# url addresses for our new restaurant
@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    # If a post request is present
    if request.method == 'POST':
        # Create a new row in our table representation
        # ID gets automatically assigned to this
        newrestaurant = Restaurant(name=request.form['name'])
        # add this new row to our database
        session.add(newrestaurant)
        # commit this change
        session.commit()
        #flash message
        flash("You created a new restaurant!")
        # redirect to the site rendered by the restaurant function
        return redirect(url_for('restaurant'))
    else:
        # else if not a post request render new restaurant again
        return render_template('newrestaurant.html')

    # This will return a template that submits a new restaurant
    return render_template('newrestaurant.html')


# url addresses for editing a restaurant
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    # Use the id to retrieve a single record from the database
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    # if a form has been posted
    if request.method == 'POST':
        # if a name has been provided
        if request.form['name']:
            # change the row name to the provided name
            editedRestaurant.name = request.form['name']
            # flash message
            flash("You edited a restaurant!")
            # send user back to the main page
            return redirect(url_for('restaurant'))
    else:
        # pass in the restaurant to be edited using the url id
        return render_template('editrestaurant.html', restaurant=editedRestaurant)


# url addresses for deleting a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    deletedrestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(deletedrestaurant)
        session.commit()
        #flash message
        flash("You deleted a new restaurant!")
        return redirect(url_for('restaurant'))
    else:
        return render_template('deleterestaurant.html', restaurant=deletedrestaurant)


# url addresses for our menu items
@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    restaurantmenus = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html', menu=restaurantmenus, restaurant=restaurant)


# url addresses for creating new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenu(restaurant_id):
    # If a post request is present
    if request.method == 'POST':
        # Create a new row in our table representation
        # ID gets automatically assigned to this
        newmenuitem = MenuItem(
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            course=request.form['course'],
            restaurant_id=restaurant_id)
        # add this new row to our database
        session.add(newmenuitem)
        # commit this change
        session.commit()
        #flash message
        flash("You created a new menu item  !")
        # redirect to the site rendered by the restaurant function
        return redirect(url_for('restaurant'))
    else:
        # else if not a post request render new restaurant again
        return render_template('newmenuitem.html', restaurant=restaurant_id)


# url addresses for editing menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenu(restaurant_id, menu_id):
    editedmenu = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedmenu.name = request.form['name']
        if request.form['description']:
            editedmenu.description = request.form['description']
        if request.form['price']:
            editedmenu.price = request.form['price']
        if request.form['course']:
            editedmenu.course = request.form['course']
        session.add(editedmenu)
        session.commit()
        #flash message
        flash("You edited a menu!")
        return redirect(url_for('restaurant'))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, editedmenu=editedmenu)


# url addresses for deleting menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenu(restaurant_id, menu_id):
    deletedmenuitem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deletedmenuitem)
        session.commit()
        #flash message
        flash("You deleted a menu item!")
        return redirect(url_for('menu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', item=deletedmenuitem)


# run only if script executed from python interpreter and not imported as a module
if __name__ == '__main__':
    # reload the server every time code changes
    app.debug = True
    # run on the local server host machine
    app.run(host = '0.0.0.0', port = 5000)