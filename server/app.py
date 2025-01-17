#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    bakery_serialized = bakery.to_dict()
    return make_response ( bakery_serialized, 200  )

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    try:    
        data = request.form
        name = data.get('name')
        price = data.get('price')
        bakery_id = data.get('bakery_id')


        if not name or not price or not bakery_id:
            return make_response({"error":"missing required fields"},400)
        new_baked_good = BakedGood(name=name,price=int(price),bakery_id =int(bakery_id))
        db.session.add(new_baked_good)
        db.session.commit()
        return make_response(new_baked_good.to_dict(),201)
    except Exception as e:
        return make_response({"error":str(e)},500)
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery_name(id):
    try:
        bakery = Bakery.query.get(id)
        if not bakery:
            return make_response({"error":"Bakery not found"},404)
        
        data = request.form
        new_name = data.get('name')

        if not new_name:
            return make_response({"error":"Name is not defined"},400)
        
        bakery.name = new_name
        db.session.commit()
        return make_response(bakery.to_dict(),200)
    except Exception as e:
        return make_response({"error":str(e)},500)

@app.route('/baked_goods/<int:id>', methods=["DELETE"])
def delete_baked_goods(id):
    try:
        baked_good =BakedGood.query.get(id)

        if not baked_good:
            return make_response({"error":"Baked goods not found"})
        db.session.delete(baked_good)
        db.session.commit()

        return make_response({"message":f"Baked good with id {id} successfully deleted"},200)
    except Exception as e:
        return make_response({"error":str(e)},500)
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)