from __future__ import annotations
from datetime import datetime, date
from enum import Enum
from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel as BaseModel, ConfigDict, Field
import sys
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


metamodel_version = "None"
version = "None"

class WeakRefShimBaseModel(BaseModel):
   __slots__ = '__weakref__'

class ConfiguredBaseModel(WeakRefShimBaseModel,
                validate_assignment = True,
                validate_all = True,
                underscore_attrs_are_private = True,
                extra = 'forbid',
                arbitrary_types_allowed = True,
                use_enum_values = True):
    pass


class IdentityEnum(str, Enum):
    
    
    identity = "identity"
    
    

class TranslationEnum(str, Enum):
    
    
    translation = "translation"
    
    

class ScaleEnum(str, Enum):
    
    
    scale = "scale"
    
    

class Image(ConfiguredBaseModel):
    
    multiscales: List[Multiscale] = Field(default_factory=list)
    

class Multiscale(ConfiguredBaseModel):
    
    version: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    axes: Optional[str] = Field(None)
    coordinateTransformations: Optional[List[Union[IdentityTransformation, ScaleTransformation, TranslationTransformation]]] = Field(default_factory=list)
    type: Optional[str] = Field(None)
    metadata: Optional[str] = Field(None)
    datasets: Optional[List[Dataset]] = Field(default_factory=list)
    

class Dataset(ConfiguredBaseModel):
    
    path: Optional[str] = Field(None)
    coordinateTransformations: Optional[List[Union[IdentityTransformation, ScaleTransformation, TranslationTransformation]]] = Field(default_factory=list)
    

class IdentityTransformation(ConfiguredBaseModel):
    
    type: IdentityEnum = Field(...)
    

class TranslationTransformation(ConfiguredBaseModel):
    
    type: TranslationEnum = Field(...)
    translation: Union[PathBasedCoordinateTransformationItem, TranslationCoordinateTransformationItem] = Field(...)
    

class ScaleTransformation(ConfiguredBaseModel):
    
    type: ScaleEnum = Field(...)
    scale: Union[PathBasedCoordinateTransformationItem, ScaleCoordinateTransformationItem] = Field(...)
    

class CoordinateTransformation(ConfiguredBaseModel):
    
    type: Optional[str] = Field(None)
    path: Optional[List[float]] = Field(default_factory=list)
    

class PathBasedCoordinateTransformationItem(ConfiguredBaseModel):
    
    path: str = Field(...)
    

class ScaleCoordinateTransformationItem(ConfiguredBaseModel):
    
    scale: List[float] = Field(default_factory=list)
    

class TranslationCoordinateTransformationItem(ConfiguredBaseModel):
    
    translation: List[float] = Field(default_factory=list)
    


# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
Image.update_forward_refs()
Multiscale.update_forward_refs()
Dataset.update_forward_refs()
IdentityTransformation.update_forward_refs()
TranslationTransformation.update_forward_refs()
ScaleTransformation.update_forward_refs()
CoordinateTransformation.update_forward_refs()
PathBasedCoordinateTransformationItem.update_forward_refs()
ScaleCoordinateTransformationItem.update_forward_refs()
TranslationCoordinateTransformationItem.update_forward_refs()

