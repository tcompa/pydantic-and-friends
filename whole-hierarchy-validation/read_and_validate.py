import zarr
from zarr.hierarchy import Group, Array
from pydantic import BaseModel  # pydantic v1
from devtools import debug
from typing import Any



class MySubgroupModel(BaseModel):
    attributes: dict[str, Any]

class MyRootGroupModel(BaseModel):
    attributes: dict[str, Any]
    members: dict[str, MySubgroupModel]


def read_whole_hierarchy_metadata(group: Group) -> dict:
    hierarchy_metadata = {}
    hierarchy_metadata["attributes"] = group.attrs.asdict()
    if not group.keys():
        return hierarchy_metadata
    hierarchy_metadata["members"] = {}
    for key in group.keys():
        sub_element = group[key]
        if isinstance(sub_element, Group):
            subgroup_hierarchy_metadata = read_whole_hierarchy_metadata(sub_element)
            hierarchy_metadata["members"][key] = subgroup_hierarchy_metadata
        elif isinstance(sub_element, Array):
            # MISSING: I should also read the .zarray content, somehow
            hierarchy_metadata["members"][key] = dict(
                attributes=sub_element.attrs.asdict()
            )
        else:
            raise ValueError(f"{key=}, {sub_element=}")
    return hierarchy_metadata


def validate_whole_hierarchy_metadata(hierarchy: dict) -> None:
    MyRootGroupModel(**hierarchy)


# EXPECTED DATA
array_metadata = dict(attributes={})
subgroup_metadata = dict(
    attributes={"key2": "value2"}, members=dict(my_array=array_metadata)
)
hierarchy_metadata = dict(
    attributes={"key": "value"}, members=dict(my_subgroup=subgroup_metadata)
)
debug(hierarchy_metadata)


root_group = zarr.open_group("my_root.zarr")
actual_hierarchy_metadata = read_whole_hierarchy_metadata(root_group)
debug(actual_hierarchy_metadata)

assert hierarchy_metadata == actual_hierarchy_metadata

validate_whole_hierarchy_metadata(actual_hierarchy_metadata)
