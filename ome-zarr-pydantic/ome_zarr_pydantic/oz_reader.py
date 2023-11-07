"""TODO: Utility functions to read data from an OME-Zarr file.
"""
import json
from pathlib import Path
from typing import Any
# from typing import Optional
import jsonschema
import requests

import dask.array as da
import numpy as np

from ome_zarr.io import parse_url  # type: ignore[import]
from ome_zarr.reader import Reader
from ome_zarr_pydantic.oz_model import OZPlate  # type: ignore[import]

from typing_extensions import Self


class PlateReader:
    __PLATE_SCHEMA_LINK: str = "https://ngff.openmicroscopy.org/0.4/schemas/plate.schema"
    __WELL_SCHEMA_LINK: str = "https://ngff.openmicroscopy.org/0.4/schemas/well.schema"
    
    plate_description: OZPlate

    # TODO: Probably create a dictionary of all images readers?

    def __init__(self: Self, path: Path) -> None:
        print('Parse plate layout')
        with Path.open(path / ".zattrs", "r") as plate_zattrs_file:
            plate_zattrs_data = json.load(plate_zattrs_file)
            
            ngff_plate_schema = json.loads(
                requests.get(self.__PLATE_SCHEMA_LINK).text
            )
            jsonschema.validate(plate_zattrs_data, ngff_plate_schema)

            self.plate_description = OZPlate(**plate_zattrs_data['plate'])
            
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
                    with Path.open(img_path / ".zattrs", "r") as img_zattrs_file:
                        img_zattrs_data = json.load(img_zattrs_file)
                        print(img_zattrs_data)


class ImageReader:
    def __init__(self: Self, path: Path) -> None:
        # TODO: Implement this
        ngff_image_schema = json.loads(
            requests.get('https://ngff.openmicroscopy.org/0.4/schemas/image.schema').text
        )
        
        # with Path.open(path / ".zattrs", "r") as zattrs_file:
        #     zattrs_data = json.load(zattrs_file)
            
        #     # zattrs_data["path"] = path  # Does the Schema validation still work?
        #     try:
        #         jsonschema.validate(zattrs_data, ngff_plate_schema)
        #         self.plate_description = OZPlate(path=path, **zattrs_data['plate'])
        #     except jsonschema.exceptions.ValidationError:
        #         # TODO: What if you expect a plate but get an image? Should be an explicit parsing option
                
        #         print('Not a plate, validating image')
        #         # TODO: Should be done more elegantly? / Probably Part of OZImage
        #         jsonschema.validate(zattrs_data, ngff_image_schema)
        #         pass


