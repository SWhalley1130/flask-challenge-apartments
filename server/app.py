from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Apartment, Tenant, Lease

app = Flask( __name__ )
app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///apartments.db'
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

migrate = Migrate( app, db )
db.init_app( app )
api = Api(app)


class AllApartments(Resource):
    def get(self):
        apts=Apartment.query.all()
        apt_dict=[a.to_dict() for a in apts]
        return make_response(jsonify(apt_dict), 200)

    def post(self):
        data=request.get_json()
        new_apt=Apartment(number=data['number'])
        db.session.add(new_apt)
        db.session.commit()
        return make_response(new_apt.to_dict(), 202)

class OneApartment(Resource):
    def get(self,id):
        apt=Apartment.query.filter(Apartment.id==id).first().to_dict()
        return make_response(jsonify(apt), 200)

    def patch(self,id):
        apt=Apartment.query.filter(Apartment.id==id).first()
        data=request.get_json()
        for attr in request.get_json():
            setattr(apt, attr, data[attr])
        db.session.add(apt)
        db.session.commit()
        return make_response(jsonify(apt.to_dict()), 200)

    def delete(self,id):
        apt=Apartment.query.filter(Apartment.id==id).first()
        leases=Lease.query.filter(Lease.apartment_id==id).all()
        for l in leases:
            db.session.delete(l)
        db.session.delete(apt)
        db.session.commit()
        return make_response({"message":"Apartment Deleted."}, 200)
    
class AllTenants(Resource):
    def get(self):
        tens=Tenant.query.all()
        tens_dict=[t.to_dict() for t in tens]
        return make_response(jsonify(tens_dict), 200)
    
    def post(self):
        data=request.get_json()
        new_ten=Tenant(name=data["name"], age=data["age"])
        db.session.add(new_ten)
        db.session.commit()
        return make_response(new_ten.to_dict(), 202)
    
class OneTenant(Resource):
    def get(self,id):
        ten=Tenant.query.filter(Tenant.id==id).first().to_dict()
        return make_response(jsonify(ten), 200)

    def patch(self,id):
        ten=Tenant.query.filter(Tenant.id==id).first()
        data=request.get_json()
        for attr in request.get_json():
            setattr(ten, attr, data[attr])
        db.session.add(ten)
        db.session.commit()
        return make_response(jsonify(ten.to_dict()), 200)

    def delete(self,id):
        ten=Tenant.query.filter(Tenant.id==id).first()
        leases=Lease.query.filter(Lease.tenant_id==id).all()
        for l in leases:
            db.session.delete(l)
        db.session.delete(ten)
        db.session.commit()
        return make_response({"message":"Tenant Deleted."}, 200)
    
    
class AllLeases(Resource):
    def get(self):
        leases=Lease.query.all()
        leases_dict=[l.to_dict() for l in leases]
        return make_response(jsonify(leases_dict), 200)

    def post(self):
        data=request.get_json()
        new_lease=Lease(
            rent=data['rent'],
            tenant_id=data['tenant_id'],
            apartment_id=data['apartment_id']
        )
        db.session.add(new_lease)
        db.session.commit()
        return make_response(new_lease.to_dict(), 202)
    
class OneLease(Resource):
    def get(self,id):
        lease=Lease.query.filter(Lease.id==id).first().to_dict()
        return make_response(jsonify(lease), 200)
    
    def delete(self,id):
        lease=Lease.query.filter(Lease.id==id).first()
        db.session.delete(lease)
        db.session.commit()
        return make_response({"message":"Lease Deleted."}, 200)
    
api.add_resource(AllApartments, '/apartments')
api.add_resource(OneApartment,'/apartments/<int:id>')
api.add_resource(AllTenants, '/tenants')
api.add_resource(OneTenant, '/tenants/<int:id>')
api.add_resource(AllLeases, '/leases')
api.add_resource(OneLease, '/leases/<int:id>')


if __name__ == '__main__':
    app.run( port = 3000, debug = True )