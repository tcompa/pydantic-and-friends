import pytest
from pathlib import Path
from ome_zarr_pydantic.oz_reader import ImageReader

from jsonschema.exceptions import ValidationError

def test_ImageReader(testdata_path: Path):
    ImageReader(testdata_path / "valid/image-01.zarr")
    ImageReader(testdata_path / "valid/image-02.zarr")

def test_ImageReader_failures(testdata_path: Path):
    ImageReader(testdata_path / "valid/image-01.zarr")
    ImageReader(testdata_path / "valid/image-02.zarr")
    with pytest.raises(ValidationError):
        ImageReader(testdata_path / "invalid/image-01.zarr")
    with pytest.raises(ValidationError):
        ImageReader(testdata_path / "invalid/image-02.zarr")
    with pytest.raises(FileNotFoundError):
        ImageReader(testdata_path / "invalid/image-03.zarr")