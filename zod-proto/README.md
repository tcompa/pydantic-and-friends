[Zod](https://zod.dev/) definitions for validation of [OME-NGFF](https://ngff.openmicroscopy.org/latest/)

## Setup

### Initial Setup

```sh
yarn init
yarn add @types/node typescript
yarn add -D ts-node
yarn tsc --init --rootDir src --outDir ./bin --esModuleInterop --lib ES2019 --module commonjs --noImplicitAny true
mkdir src
echo "console.log('Hello World\!\!\!')" > src/app.ts
# build
yarn tsc
# run
node ./bin/app.js
# or without building, run
yarn ts-node ./src/app.ts

# yarn [build|start|dev] scripts in package.json
```

### Zod Setup

Following [installation instructions](https://zod.dev/?id=installation)

Ensure `"strict": true` in `tsconfig.json`

`yarn add zod`

### Other

[example data](https://zenodo.org/records/8091756)

`yarn add zarr`
`yarn add zod`
`yarn add -D json-schema-to-zod`

## Generating Schemas

- Get json schema from [here](https://github.com/ome/ngff/tree/main/0.4/schemas)
- put in `jason_schemas/` as `<name>.schema`
- run `yarn json-schema-to-zod -s json_schemas/<name>.schema -t src/schemas/<name>Schema.ts`
- open `src/schemas/<name>Schema.ts` and change the variable name from `schema` to `<Name>Schema`
- add `export type <Name>SchemaT = z.infer<typeof <Name>Schema>;`
