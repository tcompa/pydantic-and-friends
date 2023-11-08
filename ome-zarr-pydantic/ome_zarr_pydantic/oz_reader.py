"""TODO: Utility functions to read data from an OME-Zarr file.
"""
import json
import zarr

from pathlib import Path

import jsonschema
import requests
from typing_extensions import Self

from ome_zarr_pydantic.model.image import Dataset, Image
from ome_zarr_pydantic.model.plate import Plate
from pydantic_zarr.v2 import GroupSpec


class PlateReader:
    __PLATE_SCHEMA_LINK: str = "https://ngff.openmicroscopy.org/0.4/schemas/plate.schema"
    __WELL_SCHEMA_LINK: str = "https://ngff.openmicroscopy.org/0.4/schemas/well.schema"

    plate_description: Plate
    image_readers: dict[str, "ImageReader"] = {}

    def __init__(self: Self, path: Path) -> None:
        """_summary_

        Args:
            self (Self): Class instance
            path (Path): File path to the OME-Zarr file (should be using FS to abstract location)
        """
        
        print("Parse plate layout")
        with Path.open(path / ".zattrs", "r") as plate_zattrs_file:
            plate_zattrs_data = json.load(plate_zattrs_file)

            ngff_plate_schema = json.loads(requests.get(self.__PLATE_SCHEMA_LINK).text)
            jsonschema.validate(plate_zattrs_data, ngff_plate_schema)

            self.plate_description = Plate(**plate_zattrs_data["plate"])

        for well in self.plate_description.wells:
            print(f"Parse well {well.path}")
            # TODO: What is the useful data model here?
            well_path = path / well.path

            with Path.open(well_path / ".zattrs", "r") as well_zattrs_file:
                well_zattrs_data = json.load(well_zattrs_file)

                ngff_well_schema = json.loads(requests.get(self.__WELL_SCHEMA_LINK).text)
                jsonschema.validate(well_zattrs_data, ngff_well_schema)

                for img_path_json in well_zattrs_data["well"]["images"]:
                    img_path: Path = well_path / img_path_json["path"]

                    # TODO: Change to more elegant well keys
                    self.image_readers[well.path] = ImageReader(img_path)


class ImageReader:
    """_summary_ TODO

    TODO: Only supports one multiscale for now
    TODO: Not clear about the separation of validation vs. reading
    """

    __IMAGE_SCHEMA_LINK: str = "https://ngff.openmicroscopy.org/0.4/schemas/image.schema"

    image: Image
    # chunks: dict[str, list[ZArray]] = {}

    def __init__(self: Self, path: Path) -> None:
        print("Parse image")

        ngff_image_schema = json.loads(
            requests.get("https://ngff.openmicroscopy.org/0.4/schemas/image.schema").text
        )

        with Path.open(path / ".zattrs", "r") as image_zattrs_file:
            image_zattrs_data = json.load(image_zattrs_file)

            ngff_image_schema = json.loads(requests.get(self.__IMAGE_SCHEMA_LINK).text)
            jsonschema.validate(image_zattrs_data, ngff_image_schema)

            self.image = Image(**image_zattrs_data)

        datasets: list[Dataset] = self.image.multiscales[0].datasets
        print(f"Parse zarr datasets, found {len(datasets)} datasets")

        for dataset in datasets:
            print(f"Parse dataset {dataset.path}")

            # TODO: Something wrong with the path here or the example data
            print(path/dataset.path)
            zarr_group: zarr.Group = zarr.group(path=path/dataset.path)
            
            zarr_spec = GroupSpec.from_zarr(zarr_group)
            print(zarr_spec.model_dump())
            
            
            # with Path.open(path / dataset.path / ".zarray", "r") as f:
            #     zarray_data = json.load(f)
                
                
                # self.chunks[dataset.path] = ZArray(**zarray_data)
                # print(f"Found {len(self.chunks[dataset.path].chunks)} chunks")


# # TODO: Old code below - probably can throw out the ome_zarr reader
# import dask.array as da
# import numpy as np

# from ome_zarr.io import parse_url  # type: ignore[import]
# from ome_zarr.reader import Reader, Node

# # TODO: Image Data reader based on accessor variables
# def get_image_data(  # noqa: PLR0913
#     self: Self,
#     *,
#     first_x_index: int,
#     last_x_index: int,
#     first_y_index: int,
#     last_y_index: int,
#     scale: int,
#     t: int,
#     channel: int | None,
#     label: int | None,
#     z: int,
# ) -> np.ndarray:
#     """_summary_

#     TODO: Return any kind of array, not just numpy

#     Args:
#         first_x_index (int): _description_
#         last_x_index (int): _description_
#         first_y_index (int): _description_
#         last_y_index (int): _description_
#         scale (int): _description_
#         t (int): _description_
#         channel (int | None): _description_
#         label (int | None): _description_
#         z (int): _description_

#     Raises:
#         Exception: _description_

#     Returns:
#         np.ndarray: _description_
#     """
    
#     location: ZarrLocation | None = parse_url(self.path)
#     if location is None:
#         raise Exception(f"Invalid location :{self.path}")
#     reader = Reader(location)
#     nodes: list[Node] = list(reader())
#     node_index: int = 0
#     if label is not None:
#         node_index += 2 + label
#     image_node: Node = nodes[node_index]
#     dask_data = image_node.data
#     scale_data = dask_data[scale]

#     if self.has_axe(axe_type=AxeType.t) and t is not None:
#         scale_data = scale_data[t]

#     scale_data = scale_data[channel] if channel is not None else scale_data[0]

#     image_data = scale_data[z]

#     if last_x_index > 0:
#         image_data = da.concatenate([image_data[:, :last_x_index]], axis=0)

#     if first_x_index > 0:
#         image_data = da.concatenate([image_data[:, first_x_index:]], axis=0)

#     if last_y_index > 0:
#         image_data = da.concatenate([image_data[:last_y_index, :]], axis=1)

#     if first_y_index > 0:
#         image_data = da.concatenate([image_data[first_y_index:, :]], axis=1)
#     return image_data.compute()
