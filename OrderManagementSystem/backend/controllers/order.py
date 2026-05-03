from schemas.order import OrderCreate
from sqlalchemy.orm import Session
from fastapi import HTTPException, Response
from models.product import ProductModel
from models.order import OrderModel, OrderItemsModel
from models.auth import UserModel
from models.vendor import VendorModel

def create_order(body:OrderCreate, db:Session, current_user):
    try:
        if not body.items:
            raise HTTPException(status_code=400, detail="Order must contain at least one item")

        products = db.query(ProductModel).filter(ProductModel.id.in_([item.product_id for item in body.items])).all()
        
        product_map = {p.id: p for p in products}
        total = 0

        for item in body.items:
            product = product_map.get(item.product_id)

            # check item is available or not
            if not product:
                return Response(content=f"Product {item.product_id} not found", status_code=404)

            # check the stock
            if product.quantity < item.quantity:
                return Response(content=f"Not enough stock for product {product.id}", status_code=400)
            
            # do total
            total += product.price * item.quantity

            product.quantity -= item.quantity

        order = OrderModel(
            user_id=current_user.id,
            total_amount=total,
            shipping_address=body.shipping_address
        )

        order_items = []

        for item in body.items:
            product = product_map[item.product_id]

            order_items.append(
                OrderItemsModel(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=product.price
                )
            )

        db.add(order)
        db.flush()

        for item in order_items:
            item.order_id = order.id
            db.add(item)

        db.commit()
        db.refresh(order)

        return order

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
def get_all_orders(db:Session, current_user):
    try:
        order = db.query(OrderModel).filter(OrderModel.user_id == current_user.id).all()
        return order

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def get_user_orders(db:Session, current_user):
    try:
        # 1. Get vendor
        vendor = db.query(VendorModel).filter(
            VendorModel.user_id == current_user.id
        ).first()

        if not vendor:
            raise HTTPException(status_code=404, detail="Vendor not found")

        # 2. Get order items that belong to this vendor
        order_items = db.query(OrderItemsModel).join(
            ProductModel, OrderItemsModel.product_id == ProductModel.id
        ).filter(
            ProductModel.vendor_id == vendor.id
        ).all()

        if not order_items:
            return []

        # 3. Group by order_id
        orders_map = {}

        for item in order_items:
            order = item.order

            if order.id not in orders_map:
                orders_map[order.id] = {
                    "order_id": order.id,
                    "user_id": order.user_id,
                    "total_amount": order.total_amount,
                    "shipping_address": order.shipping_address,
                    "items": []
                }

            orders_map[order.id]["items"].append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": float(item.price)
            })

        return list(orders_map.values())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))