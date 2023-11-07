"""TODO: Utility functions to read data from an OME-Zarr file.
"""
from email.policy import strict
import json
from pathlib import Path

import jsonschema
from ome_zarr_pydantic.model.image import Image
from ome_zarr_pydantic.model.plate import Plate
import requests


# TODO: Import for actual data reading later
# import dask.array as da
# import numpy as np

# from ome_zarr.io import parse_url  # type: ignore[import]
# from ome_zarr.reader import Reader


from typing_extensions import Self


class PlateReader:
    __PLATE_SCHEMA_LINK: str = "https://ngff.openmicroscopy.org/0.4/schemas/plate.schema"
    __WELL_SCHEMA_LINK: str = "https://ngff.openmicroscopy.org/0.4/schemas/well.schema"
    
    plate_description: Plate
    image_readers: dict[str, "ImageReader"] = {}

    # TODO: Probably create a dictionary of all images readers?

    def __init__(self: Self, path: Path) -> None:
        print('Parse plate layout')
        with Path.open(path / ".zattrs", "r") as plate_zattrs_file:
            plate_zattrs_data = json.load(plate_zattrs_file)
            
            ngff_plate_schema = json.loads(
                requests.get(self.__PLATE_SCHEMA_LINK).text
            )
            jsonschema.validate(plate_zattrs_data, ngff_plate_schema)

            self.plate_description = Plate(**plate_zattrs_data['plate'])
            
        for well in self.plate_description.wells:
            print(f'Parse well {well.path}')
            # TODO: What is the useful data model here?
            well_path = path / well.path
            
            with Path.open(well_path / ".zattrs", "r") as well_zattrs_file:
                well_zattrs_data = json.load(well_zattrs_file)
                
                ngff_well_schema = json.loads(
                    requests.get(self.__WELL_SCHEMA_LINK).text
                )
                jsonschema.validate(well_zattrs_data, ngff_well_schema)
                
                for img_path_json in well_zattrs_data["well"]["images"]:
                    img_path: Path = well_path / img_path_json["path"]
                    
                    # TODO: Change to more elegant well keys
                    self.image_readers[well.path] = ImageReader(img_path)


class ImageReader:
    __IMAGE_SCHEMA_LINK: str = "https://ngff.openmicroscopy.org/0.4/schemas/image.schema"
    
    image: Image
    
    def __init__(self: Self, path: Path) -> None:
        print('Parse image')
        
        ngff_image_schema = json.loads(
            requests.get('https://ngff.openmicroscopy.org/0.4/schemas/image.schema').text
        )
        
        with Path.open(path / ".zattrs", "r") as image_zattrs_file:
            image_zattrs_data = json.load(image_zattrs_file)
            
            ngff_image_schema = json.loads(
                requests.get(self.__IMAGE_SCHEMA_LINK).text
            )
            jsonschema.validate(image_zattrs_data, ngff_image_schema)

            self.image_description = Image(**image_zattrs_data)


