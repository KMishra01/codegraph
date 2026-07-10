from pydantic import BaseModel

# Input schema
class UserCreate(BaseModel):
    name: str
    age: int


# Output schema
class UserResponse(BaseModel):
    id: int
    name: str
    age: int

    class Config:
        from_attributes = True