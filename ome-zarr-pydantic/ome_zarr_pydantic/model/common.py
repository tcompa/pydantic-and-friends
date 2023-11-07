from pydantic import BaseModel

class ConfigModel(BaseModel):
    """Local Base Model for Data Classes
    """
    class Config:
        frozen = True  # Prevents mutation of the model
        strict = True  # Disables type coercion and enforces type hints