import os

import geopandas as gpd
from dotenv import load_dotenv
from shapely import make_valid
from shapely.geometry import MultiPolygon, Polygon
from sqlalchemy import create_engine


# ---------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# SOURCE DATA
# ---------------------------------------------------------

PARCEL_PATH = r"C:\Users\knigh\Downloads\GIS Sep 2026\GIS Sep 2026\Parcels.shp"


# ---------------------------------------------------------
# GEOMETRY REPAIR FUNCTION
# ---------------------------------------------------------

def repair_geometry(geometry):
    if geometry is None:
        return None

    if not geometry.is_valid:
        geometry = make_valid(geometry)

    if isinstance(geometry, Polygon):
        return MultiPolygon([geometry])

    if isinstance(geometry, MultiPolygon):
        return geometry

    if geometry.geom_type == "GeometryCollection":
        polygons = []

        for geom in geometry.geoms:

            if isinstance(geom, Polygon):
                polygons.append(geom)

            elif isinstance(geom, MultiPolygon):
                polygons.extend(list(geom.geoms))

        if polygons:
            return MultiPolygon(polygons)

    return None


# ---------------------------------------------------------
# READ PARCEL DATA
# ---------------------------------------------------------

print("Reading parcel data...")

parcels = gpd.read_file(PARCEL_PATH)

print("Records read:", len(parcels))


# ---------------------------------------------------------
# KEEP ONLY FIELDS WE NEED
# ---------------------------------------------------------

print("Cleaning parcel fields...")

parcels = parcels[
    [
        "RE",
        "STRAP",
        "Shape_STAr",
        "Shape_STLe",
        "geometry"
    ]
].copy()


# ---------------------------------------------------------
# RENAME FIELDS FOR POSTGRESQL
# ---------------------------------------------------------

parcels = parcels.rename(
    columns={
        "RE": "re",
        "STRAP": "strap",
        "Shape_STAr": "shape_area",
        "Shape_STLe": "shape_length"
    }
)


# ---------------------------------------------------------
# REPAIR GEOMETRY
# ---------------------------------------------------------

print("Repairing geometry...")

parcels["geometry"] = parcels["geometry"].apply(
    repair_geometry
)


# ---------------------------------------------------------
# CREATE UNIQUE DATABASE ID
# ---------------------------------------------------------

print("Creating parcel feature IDs...")

parcels.insert(
    0,
    "parcel_feature_id",
    range(1, len(parcels) + 1)
)


# ---------------------------------------------------------
# QA CHECKS BEFORE DATABASE LOAD
# ---------------------------------------------------------

print("\nCleaned parcel dataset")
print("----------------------")

print("Records:", len(parcels))

print("\nGeometry types:")
print(parcels.geom_type.value_counts())

print("\nInvalid geometries:")
print((~parcels.geometry.is_valid).sum())

print("\nMissing geometries:")
print(parcels.geometry.isna().sum())


# ---------------------------------------------------------
# BUILD POSTGRESQL CONNECTION
# ---------------------------------------------------------

database_url = (
    f"postgresql+psycopg://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(database_url)


# ---------------------------------------------------------
# LOAD INTO POSTGIS
# ---------------------------------------------------------

print("\nLoading parcels into PostgreSQL...")

parcels.to_postgis(
    name="parcels",
    con=engine,
    if_exists="append",
    index=False
)

print("Parcel load complete.")


# ---------------------------------------------------------
# FINISHED
# ---------------------------------------------------------

print("\nETL complete.")
