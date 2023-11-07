from enum import Enum
from gettext import translation
from ome_zarr_pydantic.model.common import ConfigModel
from pydantic import Field, model_validator, validator


class Image(ConfigModel):
    multiscales: list["Multiscale"] = Field(min_length=1)
    omero: "Omero"


class Multiscale(ConfigModel):
    axes: list["Axe"] = Field(max_length=5)  # Note: will be relaxed in v0.5
    datasets: list["Dataset"] = Field(min_length=1)
    
    @validator("axes")
    @classmethod
    def check_unique_axes(cls, value: list["Axe"]) -> list["Axe"]:
        """Check that the axes are unique.
        """
        if len(value) != len(set(value)):
            raise ValueError("Axes must be unique.")
        return value
    
    # TODO: Need to debug pydantic model_validator (see also comment below)
    # @model_validator(mode='after')
    # def check_datasets_match(self) -> None:
    #     for dataset in self.datasets:
    #         for coordinate_transformation in dataset.coordinate_transformations:
    #             if coordinate_transformation.scale != None:
    #                 if len(coordinate_transformation.scale) != len(self.axes):
    #                     raise ValueError("The scale vector dimension must match the number of axes.")
    #             if coordinate_transformation.translation != None:
    #                 if len(coordinate_transformation.translation) != len(self.axes):
    #                     raise ValueError("The translation vector dimension must match the number of axes.")


class Axe(ConfigModel):
    name: str  # The values MUST be unique across all "name" fields.
    axe_type: str = Field(alias="type")  # SHOULD be one of "space", "time" or "channel", but MAY take other values
    unit: str | None = None
    
    def __hash__(self) -> int:
        return hash(self.name)


class Dataset(ConfigModel):
    coordinate_transformations: list["CoordinateTransformation"] = Field(
        alias="coordinateTransformations",
        min_items=1,
    )
    path: str


class CoordinateTransformation(ConfigModel):
    scale: list[float] | None = None
    translation: list[float] | None = None
    transformation_type: str = Field(
        alias="type",
    )
    
    @validator("transformation_type")
    @classmethod
    def check_correct_transformation_type(cls, value: str) -> str:
        """Check that the transformation type is correct.
        
        TODO: See Enum issue below
        """
        if value not in ["identity", "translation", "scale"]:
            raise ValueError("Transformation type must be one of identity, translation or scale.")
        return value

    # TODO: Debug - for some reason this makes Pydantic return a None Object    
    # @model_validator(mode='after')
    # def check_fields(self) -> None:
    #     match self.transformation_type:
    #         case "identity":
    #             if self.scale is not None:
    #                 raise ValueError("Identity transformation cannot have a scale.")
    #             if self.translation is not None:
    #                 raise ValueError("Identity transformation cannot have a translation.")
    #         case "translation":
    #             if self.scale is not None:
    #                 raise ValueError("Translation transformation cannot have a scale.")
    #         case "scale":
    #             if self.translation is not None:
    #                 raise ValueError("Scale transformation cannot have a translation.")
    #         case _:
    #             raise ValueError("Transformation type must be one of identity, translation or scale.")
    

# TODO: Somehow the Field class doesn't play well with the Enum (even with use_enum_values = True)
# class TransformationType(Enum):
#     identity = "identity"
#     translation = "translation"
#     scale = "scale"


class Omero(ConfigModel):
    channels: list["Channel"]
    rdefs: dict | None = None  # TODO: Add Type
    version: str


class Channel(ConfigModel):
    active: bool = True
    coefficient: float = 1.0
    color: str
    family: str = "linear"
    inverted: bool = False
    label: str
    window: dict[str, int]  # TODO: Add Type
    

# TODO: Check for Zarr Pydantic Models
class ZArray(ConfigModel):
    shape: list[int]
    chunks: list[int]
    dtype: str
