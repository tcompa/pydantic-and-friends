"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const zod_1 = require("zod");
const User = zod_1.z.object({
    username: zod_1.z.string(),
});
User.parse({ username: "Ludwig" });
// { username: string }
