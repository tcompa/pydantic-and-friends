# from enum import Enum
from typing import Optional

from pydantic import Field, model_validator, validator

from ome_zarr_pydantic.model.common import ConfigModel


class Image(ConfigModel):
    multiscales: list["Multiscale"] = Field(min_length=1)
    omero: Optional["Omero"] = None


class Multiscale(ConfigModel):
    """
    Model for an element of `NgffImageMeta.multiscales`.

    See https://ngff.openmicroscopy.org/0.4/#multiscale-md.
    """
    name: Optional[str] = None
    datasets: list["Dataset"] = Field(min_length=1)
    version: Optional[str] = None
    axes: list["Axis"] = Field(min_length=2, max_length=5)  # Note: will be relaxed in v0.5

    @validator("axes")
    @classmethod
    def check_unique_axes(cls, value: list["Axis"]) -> list["Axis"]:
        """Check that the axes are unique."""
        if len(value) != len(set(value)):
            raise ValueError("Axes must be unique.")
        return value

    @model_validator(mode='after')
    def check_datasets_match(self) -> 'Multiscale':
        for dataset in self.datasets:
            for coordinate_transformation in dataset.coordinate_transformations:
                if coordinate_transformation.scale != None:
                    if len(coordinate_transformation.scale) != len(self.axes):
                        raise ValueError("The scale vector dimension must match the number of axes.")
                if coordinate_transformation.translation != None:
                    if len(coordinate_transformation.translation) != len(self.axes):
                        raise ValueError("The translation vector dimension must match the number of axes.")

        return self


class Axis(ConfigModel):
    """
    Model for an element of `Multiscale.axes`.

    See https://ngff.openmicroscopy.org/0.4/#axes-md.
    """
    name: str  # The values MUST be unique across all "name" fields.
    axe_type: Optional[str] = Field(
        alias="type"
    )  # SHOULD be one of "space", "time" or "channel", but MAY take other values
    unit: Optional[str] = None

    def __hash__(self) -> int:
        return hash(self.name)


class Dataset(ConfigModel):
    """
    Model for an element of `Multiscale.datasets`.

    See https://ngff.openmicroscopy.org/0.4/#multiscale-md
    """
    coordinate_transformations: list["CoordinateTransformation"] = Field(
        alias="coordinateTransformations",
        min_items=1,
    )
    path: str


class CoordinateTransformation(ConfigModel):
    scale: Optional[list[float]] = None
    translation: Optional[list[float]] = None
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

    @model_validator(mode='after')
    def check_fields(self) -> 'CoordinateTransformation':
        match self.transformation_type:
            case "identity":
                if self.scale is not None:
                    raise ValueError("Identity transformation cannot have a scale.")
                if self.translation is not None:
                    raise ValueError("Identity transformation cannot have a translation.")
            case "translation":
                if self.scale is not None:
                    raise ValueError("Translation transformation cannot have a scale.")
            case "scale":
                if self.translation is not None:
                    raise ValueError("Scale transformation cannot have a translation.")
            case _:
                raise ValueError("Transformation type must be one of identity, translation or scale.")
        return self


# TODO: The Enum can't be used here
# class TransformationType(Enum):
#     identity = "identity"
#     translation = "translation"
#     scale = "scale"


class Omero(ConfigModel):
    """
    Model for `NgffImageMeta.omero`.

    See https://ngff.openmicroscopy.org/0.4/#omero-md.
    """
    channels: list["Channel"]
    rdefs: Optional[dict] = None  # TODO: Add Type
    version: str


class Channel(ConfigModel):
    """
    Model for an element of `Omero.channels`.

    See https://ngff.openmicroscopy.org/0.4/#omero-md.
    """
    window: "Window"
    label: Optional[str] = None
    family: Optional[str] = None
    color: str
    active: Optional[bool] = None


class Window(ConfigModel):
    """
    Model for `Channel.window`.

    Note that we deviate by NGFF specs by making `start` and `end` optional.
    See https://ngff.openmicroscopy.org/0.4/#omero-md.
    """
    max: float
    min: float
    start: Optional[float] = None
    end: Optional[float] = None


# TODO: Check for Zarr Pydantic Models
class ZArray(ConfigModel):
    shape: list[int]
    chunks: list[int]
    dtype: str
