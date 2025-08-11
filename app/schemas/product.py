from pydantic import BaseModel, constr, confloat, conint

class Product(BaseModel):
    sku: constr(strip_whitespace=True, min_length=5)
    name: constr(strip_whitespace=True, min_length=2)
    price: confloat(gt=0)
    stock: conint(ge=0) = 0
