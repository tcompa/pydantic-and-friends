import json
from typing import Optional
import jsonschema
import math
import re
import requests
from enum import Enum
from pathlib import Path



# TODO: Check what matplotlib was used for
# from matplotlib.colors import Colormap, ListedColormap

from pydantic import BaseModel, Field, ValidationError
from typing_extensions import Self


class OZPlate(BaseModel):
    acquisitions: list
    columns: list["OZColumn"] = Field(min_items=1)
    rows: list["OZRow"] = Field(min_items=1)
    name: str | None = "Undefined"
    wells: list["OZWell"] = Field(min_items=1)


class OZColumn(BaseModel):
    name: str


class OZRow(BaseModel):
    name: str


class OZWell(BaseModel):
    path: str  # Relative path from OME Zarr
    column_index: int = Field(alias="columnIndex")
    row_index: int = Field(alias="rowIndex")


class OZImage(BaseModel):
    _creator: dict
    multiscales: list["OZMultiscale"]
    labels: list["OZLabel"] = []
    # omero: OZOmero | None = None
    # omero = None
    path: Path

    # Might not be necessary
    # class Config:
    #     arbitrary_types_allowed = True

    def __init__(self: Self, *args: str, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)

        if Path.exists(self.path / "labels"):
            with Path.open(self.path / "labels" / ".zattrs", "r") as f1:
                zattrs_data = json.load(f1)
                label_path_list = zattrs_data["labels"]
                for label_path in label_path_list:
                    label_full_path = self.path / "labels" / label_path
                    with Path.open(
                        label_full_path / ".zattrs",
                        "r",
                    ) as f2:
                        zattrs_data = json.load(f2)
                        zattrs_data["path"] = label_full_path
                        zattrs_data["name"] = label_path
                        self.labels.append(OZLabel(self, **zattrs_data))

        for multiscale in self.multiscales:
            multiscale.init(self.path, self)

class AxeType(Enum):
    t = "t"
    c = "c"
    z = "z"
    y = "y"
    x = "x"


class OZOmero(BaseModel):
    channels: list["OZChannel"]
    rdefs: dict | None = None
    version: str

    # TODO: What is this needed for?
    class Config:
        populate_by_name = True

    # TODO: Which small helpers make sense?
    def get_default_z(self: Self) -> int:
        if self.rdefs is None or self.rdefs["defaultZ"] is None:
            return 0
        return self.rdefs["defaultZ"]

    def get_default_t(self: Self) -> int:
        if self.rdefs is None or self.rdefs["defaultT"] is None:
            return 0
        return self.rdefs["defaultT"]
    

class OZMultiscale(BaseModel):
    axes: list["OZAxe"]
    datasets: list["OZDataset"]
    # The following variable are not autowired by pydantic but added by the code
    # That's why they must must have a default value (None) but they are not optional
    path: Path = None  # type: ignore[assignment]
    image: "OZImage" = None  # type: ignore[assignment]

    def init(self: Self, path: Path, image: OZImage) -> None:
        self.image = image
        self.path = path
        for i, dataset in enumerate(self.datasets):
            dataset.init(self, self.path, i)


class OZDataset(BaseModel):
    transformations: list["OZCoordinateTransformation"] = Field(
        alias="coordinateTransformations",
    )  # don't want to use 'type' as a variable name

    # The following variable are not autowired by pydantic but added by the code
    # That's why they must must have a default value (None) but they are not optional
    path: Path = None  # type: ignore[assignment]
    index: int = None  # type: ignore[assignment]
    zarray: "ZArray" = None  # type: ignore[assignment]
    parent: "OZMultiscale" = None  # type: ignore[assignment]
    image: "OZImage" = None  # type: ignore[assignment]

    class Config:
        populate_by_name = True

    def init(
        self: Self,
        parent: OZMultiscale,
        path: Path,
        index: int,
    ) -> None:
        self.parent = parent
        self.path = Path(path) / str(index)
        self.index = index
        self.image = parent.image
        with Path.open(self.path / ".zarray", "r") as f:
            zarray_data = json.load(f)
            self.zarray = ZArray(**zarray_data)

    def get_axe_size(self: Self, axe: AxeType) -> int | None:
        index = self.image.get_axe_index(axe=axe)
        if index is not None:
            return self.zarray.shape[index]
        return None

    def get_chunks_count(self: Self, axe: AxeType) -> int:
        index = self.image.get_axe_index(axe)
        if index is None:
            return 0
        return math.ceil(self.zarray.shape[index] / self.zarray.chunks[index])

    def get_pixel_index_for_position(self: Self, x: float, y: float) -> dict[str, int]:
        """Returns the position index of the given coordinate along the specified axis.

        Args:
        ----
        x (float): The coordinate value along x axis.
        y (float): The coordinate value along y axis.

        """
        index_axe_x = self.image.get_axe_index(AxeType.x)
        index_axe_y = self.image.get_axe_index(AxeType.y)

        if index_axe_x is None or index_axe_y is None:
            raise Exception("x or y axis not found")

        transformation = self.transformations[0]
        if transformation.scale is None:
            raise Exception("scale not found")

        resolution_x = self.image.get_pixels_size()[AxeType.x]
        scale_x = transformation.scale[index_axe_x]
        pixel_size_x = resolution_x * scale_x
        index_x = math.floor(x / pixel_size_x)

        resolution_y = self.image.get_pixels_size()[AxeType.y]
        scale_y = transformation.scale[index_axe_y]
        pixel_size_y = resolution_y * scale_y
        index_y = math.floor(y / pixel_size_y)

        return {
            "x": index_x,
            "y": index_y,
        }


class OZCoordinateTransformation(BaseModel):
    scale: list[float] | None = None
    translation: list[float] | None = None
    transformation_type: str = Field(
        alias="type",
    )  # don't want to use 'type' as a variable name

    class Config:
        populate_by_name = True


class ZArray(BaseModel):
    shape: list[int]
    chunks: list[int]
    dtype: str


class OZAxe(BaseModel):
    axe_type: str = Field(alias="type")  # don't want to use 'type' as a variable name
    name: AxeType
    unit: str | None = None

    class Config:
        populate_by_name = True


class OZImageLabel(BaseModel):
    colors: list["OZColor"]
    properties: list
    version: str


class OZColor(BaseModel):
    label_value: int = Field(alias="label-value")
    rgba: list[int]

    class Config:
        populate_by_name = True


class OZLabel(BaseModel):
    name: str
    image_label: OZImageLabel = Field(alias="image-label")
    multiscales: list["OZMultiscale"]

    # The following variable are not autowired by pydantic but added by the code
    # That's why they must must have a default value (None) but they are not optional
    path: Path = None  # type: ignore[assignment]

    class Config:
        populate_by_name = True

    def __init__(self: Self, parent: OZImage, *args: str, **kwargs: str) -> None:
        super().__init__(*args, **kwargs)
        for multiscale in self.multiscales:
            multiscale.init(self.path, parent)

    def info(self: Self) -> str:
        info = f"label info: {self.path}\n"
        for scale in self.get_datasets():
            info += f"    scale {scale.index},{scale.path} :\n"
            info += f"      t size: {scale.get_axe_size(AxeType.t)}\n"
            info += f"      c size: {scale.get_axe_size(AxeType.c)}\n"
            info += f"      z size: {scale.get_axe_size(AxeType.z)}\n"
            info += f"      y size: {scale.get_axe_size(AxeType.y)}\n"
            info += f"      x size: {scale.get_axe_size(AxeType.x)}\n"
        return info

    def get_datasets(self: Self) -> list["OZDataset"]:
        return self.multiscales[0].datasets

    def get_property_names(self: Self) -> list[str]:
        property_names = set()
        for d in self.image_label.properties:
            for key in d:
                property_names.add(key)
        return list(property_names)

    def get_max_color(self: Self) -> int:
        max_color = 0
        for color in self.image_label.colors:
            if color.label_value > max_color:
                max_color = color.label_value
        return max_color

    # def get_cmap(self: Self) -> Colormap:
    #     cmaplist = []

    #     # fill with transparent colors
    #     for _ in range(self.get_max_color() + 1):
    #         cmaplist.append((0.0, 0.0, 0.0, 0.0))  # noqa: PERF401

    #     for color in self.image_label.colors:
    #         cmaplist[color.label_value] = (
    #             color.rgba[0] / 256,
    #             color.rgba[1] / 256,
    #             color.rgba[2] / 256,
    #             1,  # we ignore the alpha value from the file
    #         )

    #     return ListedColormap(cmaplist)


class OZChannel(BaseModel):
    active: bool = True
    coefficient: float = 1.0
    color: str
    family: str = "linear"
    inverted: bool = False
    label: str
    window: dict[str, int]

    class Config:
        populate_by_name = True

    def set_hex_color(self: Self, hex_color: str) -> None:
        if bool(re.match("^#[0-9a-fA-F]{6}$", hex_color)):
            self.color = hex_color[1:]

    def get_hex_color(self: Self) -> str:
        return "#" + self.color