# GDAL Native Runtime

This directory must be populated with native DLLs from the
**MaxRev.Gdal.Core 3.3.3.120** NuGet package before using this package
with .NET assemblies that depend on GDAL 3.3.3.

## How to populate

1. Download or locate the NuGet package. The easiest source is the Orchid
   .NET build output:

       D:\source\Orchid\Orchid\Orchid.Application\bin\x64\Debug\runtimes\win-x64\native\

   (Substitute `Release` for `Debug` if you built in Release configuration.)

2. Copy the entire contents of that `native\` folder into **this** directory:

   - All `*.dll` files (gdal303.dll, osr_wrap.dll, gdal_wrap.dll, etc.)
   - The `gdalplugins\` subfolder (contains gdal_HDF4.dll, gdal_HDF5.dll)
   - The `maxrev.gdal.core.libshared\` subfolder (contains proj.db)

   Resulting layout:
   ```
   orchid/_native/gdal/
     gdal303.dll
     osr_wrap.dll
     gdal_wrap.dll
     gdalconst_wrap.dll
     ogr_wrap.dll
     ... (all other *.dll files)
     gdalplugins/
       gdal_HDF4.dll
       gdal_HDF5.dll
     maxrev.gdal.core.libshared/
       proj.db
   ```

   The folder contains approximately 50 DLLs in total; simply copy all
   `*.dll` files from `native\` — no need to cherry-pick.

3. **Note on `gdal-data/`:** The MaxRev.Gdal.Core 3.3.3.120 native folder
   does **not** include a `gdal-data/` directory — it contains only DLLs,
   `gdalplugins/`, and `maxrev.gdal.core.libshared/`. For GDAL 3.3.3, the
   required data files are typically embedded in the DLL, so most users will
   not need `GDAL_DATA` at all. If you do need it (e.g., for custom
   projections), manually create a `gdal-data/` subdirectory here and
   populate it; the bootstrapper will then set `GDAL_DATA` automatically if
   it finds `orchid/_native/gdal/gdal-data/` at runtime.

## Environment variables set by the bootstrapper

| Variable   | Value                                                  |
|------------|--------------------------------------------------------|
| GDAL_DATA  | `<this dir>/gdal-data` (only if you manually add that subdir; not present in the MaxRev.Gdal.Core 3.3.3.120 build output) |
| PROJ_LIB   | `<this dir>/maxrev.gdal.core.libshared`               |

## Why these DLLs are not committed

The native DLLs total ~100 MB and are Windows/architecture-specific.
They are excluded by `.gitignore`. Once the vendor strategy is confirmed
working, the team will decide on a long-term distribution mechanism
(e.g., fetching from the NuGet package at build time).
