"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const zod_1 = require("zod");
// creating a schema for strings
const mySchema = zod_1.z.string();
// parsing
mySchema.parse("tuna"); // => "tuna"
mySchema.parse(12); // => throws ZodError
// "safe" parsing (doesn't throw error if validation fails)
mySchema.safeParse("tuna"); // => { success: true; data: "tuna" }
mySchema.safeParse(12); // => { success: false; error: ZodError }
