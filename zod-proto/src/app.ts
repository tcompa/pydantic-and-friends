import * as fs from "fs";
import { openGroup } from "zarr";
import { FileStore } from "./util/store.js";
import { PlateSchema, PlateSchemaT } from "./schemas/plateSchema.js";

const zarrName = "20200812-CardiomyocyteDifferentiation14-Cycle1";
//const files = await fs.promises.readdir(`data/${zarrName}.zarr`);
const zarrStore = new FileStore("/", `data/${zarrName}.zarr`);
const rootGroup = await openGroup(zarrStore, zarrStore.rootName, "r");
const rootAttr = await rootGroup.attrs.asObject();
const res = PlateSchema.parse(rootAttr);

console.log("done");
