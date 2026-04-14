from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin: str

class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address

address_dict = {'city':'surat', 'state':'gujarat', 'pin':'123456'}
address1 = Address(**address_dict)
patient_dict = {'name':'krishi', 'gender':'female', 'age':20, 'address':address1}
patient1 = Patient(**patient_dict)

temp = patient1.model_dump_json()
print(temp)
print(type(temp))


# field_validator
# model_validator
# computed fields
# nested models
# dump to json - serialization



# Request body
# use Pydantic BaseModel for the data validation
# class Item(BaseModel):
#     name: str
#     price: float
#     email: EmailStr
#     oficail_web: AnyUrl
#     availabe: bool = True
#     tax: float | None = None
#     colors: Optional[List[str]] = None
#     item_details: Dict[str, str]

class Item(BaseModel):
    name: Annotated[str, Field(max_length=50)]
    price: Annotated[float, Field(gt=0)]
    email: Annotated[EmailStr, Field(title="Official email of the company")]
    oficail_web: Annotated[AnyUrl, Field(title="Official website url", default=None)]
    availabe: Annotated[bool, Field(default=True, title="Item available or not")]
    tax: Annotated[float, Field(default=None, strict=True)]
    colors: Annotated[Optional[List[str]], Field(default=None)]
    item_details: Annotated[Dict[str, str], Field(default=None)]
    discount: Annotated[Optional[float], Field(default=None, gt=0, lt=100)]
    contact_details : Annotated[Optional[Dict[str, str]], Field(default=None)]

    @model_validator(mode='after')
    def age_validator(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError("Emergency contact details are required for age above 60")
        
        return model

    @field_validator('name')
    @classmethod
    def name_validator(cls, value):
        return value.upper()

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'icici.com', 'gmail.com']
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError("Not a valid domain")
        
        return value

    @computed_field
    @property
    def price_with_tax(self) -> Optional[float]:
        if self.tax is not None:
            return self.price + (self.price * self.tax / 100)
        return None

# request body
# {
#   "name": "Mobile",
#   "price": 200.5,
#   "colors": ["black", "white", "blue"],
#   "item_details": {
#     "height": "20 inches",
#     "weight": "2 kg"
#   }
# }


@app.post("/items/")
async def create_item(item: Item):
    return item


# path parameters
@app.get("/items/{item_id}")
def get_item(item_id:int):
    return f"This is the item id {item_id}"

# query params
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
