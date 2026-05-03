from schemas.product import ProductSchema, CatgorySchema, ProductUpdateSchema
from sqlalchemy.orm import Session
from models.product import ProductModel, CategoryModel
from models.vendor import VendorModel
from fastapi import HTTPException, Response

# product category apis
def add_category(body:CatgorySchema, db:Session, current_user):
    try:
        is_catrgory = db.query(CategoryModel).filter(CategoryModel.name == body.name).first()
        if is_catrgory:
            return Response(content="Category already exist", status_code=400)
        
        category = CategoryModel(name = body.name)

        db.add(category)
        db.commit()
        db.refresh(category)

        return Response(content="Category Added Successfully!", status_code=201)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
def get_category(db:Session, current_user):
    try:
        categories = db.query(CategoryModel).all()
        return categories

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# product apis
def add_product(body:ProductSchema, db:Session, current_user):
    try:
        # 1. Check category exists
        category = db.query(CategoryModel).filter(
            CategoryModel.id == body.category_id
        ).first()

        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        # 2. Get vendor (assuming 1-1 with user)
        vendor = db.query(VendorModel).filter(
            VendorModel.user_id == current_user.id
        ).first()

        if not vendor:
            raise HTTPException(status_code=403, detail="Vendor not found")
        
        product = ProductModel(
            name=body.name,
            image_url=str(body.image_url) if body.image_url else None,
            description=body.description,
            price=body.price,
            quantity=body.quantity,
            category_id=body.category_id,
            vendor_id=vendor.id
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
def get_product(db:Session, current_user):
    try:
        vendor = db.query(VendorModel).filter(
            VendorModel.user_id == current_user.id
        ).first()

        if not vendor:
            raise HTTPException(status_code=403, detail="Vendor not found")
        
        products = db.query(ProductModel).filter(ProductModel.vendor_id == vendor.id).all()
        return products

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def get_all_product(db:Session, current_user):
    try:
        products = db.query(ProductModel).all()
        return products

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def update_product(id:int, body:ProductUpdateSchema, db:Session, current_user):
    try:
        product = db.query(ProductModel).filter(ProductModel.id == id).first()
        if not product:
            return Response(content="Product not found!", status_code=404)
        
        update_data = body.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(product, key, value)

        db.commit()
        db.refresh(product)

        return product

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
def delete_product(id:int, db:Session, current_user):
    try:
        product = db.query(ProductModel).filter(ProductModel.id == id).first()
        if not product:
            return Response(content="Product not found!", status_code=404)
        
        db.delete(product)
        db.commit()

        return Response(content="Product deleted successfully!", status_code=200)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
