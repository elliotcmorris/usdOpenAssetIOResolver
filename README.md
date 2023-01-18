# usdOpenAssetIOResolver

An AR2 plugin that hosts OpenAssetIO

## Building

```sh
cmake -S . -B build
cmake --build build
cmake --install build
```

> **Note**
>
> USD is found by searching for `pxrConfig.cmake` in the USD install dir.
> If USD is on your system path, this should be found automatically.
> If for some reason you can't set or inherit the system path, you can
> add the USD install dir to `CMAKE_PREFIX_PATH`.

## Running

```sh
export PXR_PLUGINPATH_NAME=$(pwd)/build/dist/resources/plugInfo.json
usdcat yourUsdFile.usd
```

## Debug logging

Before running any USD application

```sh
export TF_DEBUG=OPENASSETIO_RESOLVER
```

To enable debug logging from the resolver.

## Testing

To run tests, from the project root

```sh
cd tests
python -m pip install -r requirements.txt
pytest
```
