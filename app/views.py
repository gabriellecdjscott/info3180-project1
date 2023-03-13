"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

from app import app
from flask import render_template, request, redirect, url_for, flash
from .forms import PropertyForm
import os
from app import app, db
from werkzeug.utils import secure_filename
from .models import Properties
from operator import length_hint


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route("/properties/create",methods=['POST', 'GET'])
def create():
    propForm = PropertyForm()
    
    if request.method == 'GET':
        return render_template("createProperty.html",form=propForm)
        
    if request.method == 'POST' and propForm.validate_on_submit():
        
        #photo =  myform.photo.data  
        #filename = secure_filename(photo.filename)
       
        
        title = propForm.title.data
        bedNum = propForm.bedNum.data
        bathNum = propForm.bathNum.data
        location = propForm.location.data
        propType = propForm.propType.data
        price = propForm.price.data
        descr =  propForm.descr.data
        
        photo=propForm.pic.data
        filename=secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        propinfo = Properties(title=title , 
                                    bedNum=bedNum, bathNum = bathNum, 
                                    location = location, PropType = propType,
                                    price = price, descr= descr, photo = filename) 
        
        db.session.add(propinfo)
        db. session.commit()

        flash('Successfully added a new property','success')
        return redirect(url_for('DisplayProp'))
    else:
        flash('Property not added','danger')
        
    flash_errors(propForm)
    return render_template('createProperty.html', form = propForm)
    
@app.route('/properties')
def DisplayProp():
    
    photos= get_uploaded_images()
    if get_prop_info() != []:
        rootdir = 'uploads/'
        length =length_hint(get_prop_info())
        return render_template('allProp.html', filenames= photos , properties= get_prop_info() ,rootdirectory = rootdir, len = length)
    else: 
        flash("No properties", 'danger')
        return redirect('allProp.html')

def get_uploaded_images():
    rootdir = os.getcwd()
    file_lst=[]
    print("root directry:",rootdir)
    for subdir, dirs, files in os.walk('uploads/'):
        for file in files:
            file_lst.append(os.path.join(subdir, file))
    return file_lst

def get_prop_info():
    properties= Properties.query.all()
    return properties

@app.route('/properties/<int:id>')
def viewProp(id):
    view_prop = Properties.query.get_or_404(id)
    return render_template('property.html', prop = view_prop,rootdiri = 'uploads/')   
###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")