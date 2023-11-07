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
