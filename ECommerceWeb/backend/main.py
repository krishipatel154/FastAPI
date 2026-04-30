from fastapi import FastAPI, Request
from mockData import products
from dtos import Product

app = FastAPI()

@app.get("/")
def home():
    return "hello"

@app.get("/products")
def get_products():
    return products

@app.get("/product/{id}")
def product(id: int):
    product = None
    for i in products:
        if i.get("id") == id:
            return i
    
    return {
        "error": "product not found"
    }

@app.get("/greet")
def greet_user(request:Request):
    query_params = dict(request.query_params)
    return {
        "greet": f"Hello, {query_params.get('name')}"
    }

@app.post("/create-product")
def create_product(product: Product):
    product = product.model_dump()
    products.append(product)
    return {
        "payload":products,
        "message":"Product created successfully!"
    }

@app.put("/update-product/{id}")
def update_product(product: Product, id: int):

    for index, oneProduct in enumerate(products):
        if oneProduct.get("id") == id:
            products[index] = product.model_dump()
            return {
                "payload":product,
                "message":"Product updated successfully!"
            }

    return {
        "message":"Product not found"
    }

@app.delete("/delete-product/{id}")
def delete_product(id:int):
    for index, oneProduct in enumerate(products):
        if oneProduct.get("id") == id:
            deleted_product = products.pop(index)
            return {
                "payload":deleted_product,
                "message":"Product deleted successfully!"
            }

    return {
        "message":"Product not found"
    }