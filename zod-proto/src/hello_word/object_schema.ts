import { z } from "zod";

export const User = z.object({
  username: z.string(),
});

User.parse({ username: "Ludwig" });

// extract the inferred type
export type User = z.infer<typeof User>;
// { username: string }
