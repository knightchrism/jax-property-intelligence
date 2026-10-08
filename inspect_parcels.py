import geopandas as gpd

from shapely.validation import explain_validity

from shapely import make_valid

parcels = gpd.read_file(r"C:\Users\knigh\Downloads\GIS Sep 2026\GIS Sep 2026\Parcels.shp")

print("Number of records:")
print(len(parcels))

print("\nColumns:")
print(parcels.columns.tolist())

print("\nCoordinate system:")
print(parcels.crs)

print("\nFirst 5 records:")
print(parcels.head())

print("\nGeometry types:")
print(parcels.geom_type.value_counts())
print("\nMissing RE values:")
print(parcels["RE"].isna().sum())

print("\nMissing STRAP values:")
print(parcels["STRAP"].isna().sum())

print("\nDuplicate RE values:")
print(parcels["RE"].duplicated().sum())

print("\nDuplicate STRAP values:")
print(parcels["STRAP"].duplicated().sum())

print("\nInvalid geometries:")
print((~parcels.geometry.is_valid).sum())

print("\nEmpty geometries:")
print(parcels.geometry.is_empty.sum())

print("\nDuplicate RE records:")
print(
    parcels[parcels["RE"].duplicated(keep=False)]
    [["RE", "STRAP", "geometry"]]
)

print("\nDuplicate STRAP records:")
print(
    parcels[parcels["STRAP"].duplicated(keep=False)]
    [["RE", "STRAP", "geometry"]]
)

print("\nInvalid geometry records:")
print(
    parcels[~parcels.geometry.is_valid]
    [["RE", "STRAP", "geometry"]]
)


invalid_parcels = parcels[~parcels.geometry.is_valid].copy()

invalid_parcels["validity_reason"] = invalid_parcels.geometry.apply(
    explain_validity
)

print("\nInvalid geometry reasons:")
print(
    invalid_parcels[
        ["RE", "STRAP", "validity_reason"]
    ]
)

invalid_parcels = parcels[~parcels.geometry.is_valid].copy()

invalid_parcels["fixed_geometry"] = invalid_parcels.geometry.apply(make_valid)

print("\nGeometry validity after repair:")
print(invalid_parcels["fixed_geometry"].is_valid.value_counts())

print("\nGeometry types after repair:")
print(invalid_parcels["fixed_geometry"].geom_type.value_counts())
