from . import db

class Properties(db.Model):

     __tablename__ = 'properties'

     propertyId = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(180),nullable=False)
     location = db.Column(db.String(280),nullable=False)
     bathNum = db.Column(db.Integer,nullable=False)
     bedNum = db.Column(db.Integer,nullable=False)
     price = db.Column(db.Integer,nullable=False)
     PropType = db.Column(db.String(15))
     descr = db.Column(db.String(800))
     photo= db.Column(db.Text,nullable=False)


     def __init__(self,title, location,bathNum,bedNum, price,PropType,descr,photo):
         self.title = title 
         self.location = location
         self.bathNum = bathNum
         self.bedNum = bedNum
         self.price = price  
         self.PropType = PropType
         self.photo= photo
         self.descr = descr
