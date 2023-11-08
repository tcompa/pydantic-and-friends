import * as fs from "fs";
import { KeyError } from "zarr";
import { AsyncStore } from "zarr/types/storage/types";

/**
 * Preserves (double) slashes earlier in the path, so this works better
 * for URLs. From https://stackoverflow.com/a/46427607/4178400
 * @param args parts of a path or URL to join.
 */
function joinUrlParts(...args: string[]) {
  return args
    .map((part, i) => {
      if (i === 0) return part.trim().replace(/[/]*$/g, "");
      return part.trim().replace(/(^[/]*|[/]*$)/g, "");
    })
    .filter((x) => x.length)
    .join("/");
}

class ReadOnlyStore {
  async keys() {
    return [];
  }

  async deleteItem() {
    return false;
  }

  async setItem() {
    console.warn("Cannot write to read-only store.");
    return false;
  }
}

export class FileStore
  extends ReadOnlyStore
  implements AsyncStore<ArrayBuffer>
{
  private _rootPrefix: string;
  private _rootName: string;

  constructor(rootName: string, rootPrefix = "") {
    super();
    this._rootPrefix = rootPrefix;
    this._rootName = rootName;
  }

  get rootName() {
    return this._rootName;
  }

  private _key(key: string) {
    return joinUrlParts(this._rootPrefix, key);
  }

  async getItem(key: string) {
    const path = this._key(key);
    if (!path) {
      throw new KeyError(key);
    }
    const buffer = await fs.promises.readFile(path);
    return buffer;
  }

  async containsItem(key: string) {
    const path = this._key(key);
    const exists = fs.existsSync(path);
    return exists;
  }
}
