from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_restful import Api, Resource
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}) 

db = SQLAlchemy(metadata=metadata)

class Tenant(db.Model, SerializerMixin):
    __tablename__="tenants"

    serialize_rules=("-ten_leases.ten_backref",)

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, nullable=False)
    age=db.Column(db.Integer)

    ten_leases=db.relationship('Lease', backref='ten_backref')

    @validates('age')
    def age_validation(self, key, value):
        if value>17:
            return value
        else:
            raise Exception('Must be 18 or older.')
        
    @validates('name')
    def name_validation(self, key, value):
        if value =="":
            raise Exception('Name is required.')
        else:
            return value
        

###LEASES IS THE JOIN TABLE###
class Lease(db.Model, SerializerMixin):
    __tablename__="leases"

    serialize_rules=("-ten_backref.ten_leases", "-apt_backref.apt_leases",)
    
    id=db.Column(db.Integer, primary_key=True)
    rent=db.Column(db.Integer)

    tenant_id=db.Column(db.Integer, db.ForeignKey('tenants.id'))
    apartment_id=db.Column(db.Integer, db.ForeignKey('apartments.id'))


class Apartment(db.Model, SerializerMixin):
    __tablename__="apartments"

    serialize_rules=("-apt_leases.apt_backref",)

    id=db.Column(db.Integer, primary_key=True)
    number=db.Column(db.Integer)

    apt_leases=db.relationship('Lease', backref="apt_backref")


