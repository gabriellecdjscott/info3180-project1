from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, IntegerField
from wtforms.validators import InputRequired, DataRequired , Length
from flask_wtf.file import FileField, FileRequired, FileAllowed


class PropertyForm(FlaskForm):
     title = StringField('Title', validators=[InputRequired()])
     bedNum = IntegerField('Bedrooms', validators=[InputRequired()])
     bathNum= IntegerField('Bathrooms', validators=[InputRequired()])
     location= StringField('Location', validators=[InputRequired()])
     price=IntegerField('Price', validators=[InputRequired()])

     propType=SelectField("Type", choices=[("Apt", "Apartment"),("House", "House")])
     descr=TextAreaField("Description",validators=[DataRequired(),InputRequired(),Length(max=700)])

     pic=FileField("Photo", validators=[FileRequired(),FileAllowed(["jpg", "png","jpeg","Images only!"])])