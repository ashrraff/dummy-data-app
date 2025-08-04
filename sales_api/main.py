from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from . import models, schemas, database


# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Sales API")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Customers

@app.post("/customers", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = db.query(models.Customer).filter(models.Customer.email == customer.email).first()
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_customer = models.Customer(**customer.model_dump())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@app.get("/customers/{customer_id}", response_model=schemas.Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.get("/customers", response_model=list[schemas.Customer])
def list_customers(db: Session = Depends(get_db)):
    return db.query(models.Customer).all()


# Products

@app.post("/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.get("/products", response_model=list[schemas.Product])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


# Sales

@app.post("/sales", response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == sale.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    customer = db.query(models.Customer).filter(models.Customer.id == sale.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    new_sale = models.Sale(**sale.model_dump())
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return new_sale


@app.get("/sales", response_model=list[schemas.Sale])
def list_sales(db: Session = Depends(get_db)):
    sales_list = db.query(models.Sale).options(joinedload(models.Sale.products)).all()
    response_sales = []
    for sale in sales_list:
        total_price = 0
        if sale.products: # Ensure the product was loaded and exists for this sale
            total_price = sale.products.price * sale.quantity

        # Manually create an instance of SaleGet, passing all necessary fields
        response_sales.append(schemas.Sale(
            id=sale.id,
            customer_id=sale.customer_id,
            product_id=sale.product_id,
            quantity=sale.quantity,
            timestamp=sale.timestamp,
            total_price=total_price))
        
    return response_sales