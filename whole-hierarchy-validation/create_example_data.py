import zarr

root = zarr.open_group("my_root.zarr", "w")
root.attrs.put({"key": "value"})

subgroup = root.create_group("my_subgroup")
subgroup.attrs.put({"key2": "value2"})

zarr.open_array(
    "my_root.zarr/my_subgroup/my_array",
    shape=(1000, 1000),
    chunks=(100, 100),
)
