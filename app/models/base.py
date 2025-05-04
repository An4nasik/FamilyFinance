from pydantic import BaseModel as PydanticBaseModel
from bson import ObjectId
from datetime import date
class BaseModel(PydanticBaseModel):
    model_config = {
        "json_schema_extra": {},
        "populate_by_name": True,
        "json_encoders": {ObjectId: str},
        "arbitrary_types_allowed": True,
    }

