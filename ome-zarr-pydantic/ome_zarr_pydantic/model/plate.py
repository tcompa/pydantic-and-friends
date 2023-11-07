from pydantic import Field, validator

from ome_zarr_pydantic.model.common import ConfigModel


class Plate(ConfigModel):
    acquisitions: list
    columns: list["Column"] = Field(min_items=1)
    rows: list["Row"] = Field(min_items=1)
    name: str | None = "Undefined"
    wells: list["Well"] = Field(min_items=1)

    @validator("columns")
    @classmethod
    def check_unique_columns(cls, value: list["Column"]) -> list["Column"]:
        """Check that the columns are unique."""
        if len(value) != len(set(value)):
            raise ValueError("Columns must be unique.")
        return value

    @validator("rows")
    @classmethod
    def check_unique_rows(cls, value: list["Row"]) -> list["Row"]:
        """Check that the rows are unique."""
        if len(value) != len(set(value)):
            raise ValueError("Rows must be unique.")
        return value

    @validator("wells")
    @classmethod
    def check_unique_wells(cls, value: list["Well"]) -> list["Well"]:
        """Check that the wells are unique."""
        if len(value) != len(set(value)):
            raise ValueError("Wells must be unique.")
        return value


class Column(ConfigModel):
    name: str


class Row(ConfigModel):
    name: str


class Well(ConfigModel):
    path: str  # Relative path from OME Zarr
    column_index: int = Field(alias="columnIndex")
    row_index: int = Field(alias="rowIndex")
