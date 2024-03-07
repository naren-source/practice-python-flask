import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import models
from db import db
from sqlalchemy.exc import SQLAlchemyError
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = models.ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = models.ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": f"Item {item.name} Deleted"}        

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemUpdateSchema)
    def put(self, item_data, item_id):
        item = models.ItemModel.query.get(item_id)

        if item:
            item.price = item_data['price']
            item.name = item_data['name']
        else:
            item = models.ItemModel(id=item_id,**item_data)

        db.session.add(item)
        db.session.commit()
        return item


@blp.route("/item")
class ItemList(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return models.ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = models.ItemModel(**item_data)
        print(item)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")
        return item



