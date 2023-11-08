import os
from os.path import dirname
from pathlib import Path

from ome_zarr_pydantic.oz_reader import PlateReader


def main() -> None:
    # HACK: Fixed path to the test dataset
    script_dir = dirname(dirname(__file__))
    test_data_location = os.path.join(
        script_dir, "resources", "20200812-CardiomyocyteDifferentiation14-Cycle1.zarr"
    )

    # Set data path
    test_data_path: Path = Path(test_data_location)

    if not test_data_path.exists():
        raise ValueError(f"The path, {test_data_location}, to the data does not exist.")

    if not test_data_path.suffix == ".zarr":
        raise ValueError(f"The path, {test_data_location}, to the data is not a zarr file.")

    test_file = PlateReader(test_data_path)

    print(test_file)


if __name__ == "__main__":
    main()
