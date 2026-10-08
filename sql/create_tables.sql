-- =========================================================
-- JAX PROPERTY INTELLIGENCE
-- DATABASE STRUCTURE
-- =========================================================


-- ---------------------------------------------------------
-- PARCELS TABLE
-- ---------------------------------------------------------

CREATE TABLE IF NOT EXISTS parcels (
    parcel_feature_id BIGINT PRIMARY KEY,
    re VARCHAR(20) NOT NULL,
    strap VARCHAR(20) NOT NULL,
    shape_area DOUBLE PRECISION,
    shape_length DOUBLE PRECISION,
    geometry geometry(MultiPolygonZ, 2236)
);


-- ---------------------------------------------------------
-- PARCEL INDEXES
-- ---------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_parcels_re
ON parcels (re);

CREATE INDEX IF NOT EXISTS idx_parcels_strap
ON parcels (strap);

CREATE INDEX IF NOT EXISTS idx_parcels_geometry
ON parcels
USING GIST (geometry);


-- ---------------------------------------------------------
-- PROPERTIES TABLE
-- ---------------------------------------------------------

CREATE TABLE IF NOT EXISTS properties (
    strap VARCHAR(20) PRIMARY KEY,
    section VARCHAR(10),
    township VARCHAR(10),
    range_code VARCHAR(10),
    tile_number VARCHAR(20),
    confidentiality_flag VARCHAR(10),

    mailing_address_1 VARCHAR(255),
    mailing_address_2 VARCHAR(255),
    mailing_city VARCHAR(100),
    mailing_state VARCHAR(10),
    mailing_zip VARCHAR(20),

    property_use_code VARCHAR(20),
    subdivision_number VARCHAR(20),
    subdivision_name VARCHAR(255),
    plat_book VARCHAR(20),
    plat_page VARCHAR(20),

    neighborhood_code VARCHAR(50),
    percent_capped DOUBLE PRECISION,
    valuation_method VARCHAR(20),
    cap_base_year INTEGER,

    total_market_value NUMERIC,
    assessed_value NUMERIC,
    building_value NUMERIC,
    total_just_value NUMERIC,

    school_taxable NUMERIC,
    county_municipal_taxable NUMERIC,
    sjrwmd_taxable NUMERIC,

    taxing_district_code VARCHAR(20),
    gis_square_feet BIGINT,
    documented_acres DOUBLE PRECISION
);


-- ---------------------------------------------------------
-- PROPERTY SUMMARY VIEW
-- ---------------------------------------------------------

CREATE OR REPLACE VIEW property_summary AS
SELECT
    p.parcel_feature_id,
    p.re,
    p.strap,
    pr.property_use_code,
    pr.total_market_value,
    pr.assessed_value,
    pr.building_value,
    pr.total_just_value,
    pr.documented_acres,
    pr.mailing_address_1,
    pr.mailing_address_2,
    pr.mailing_city,
    pr.mailing_state,
    pr.mailing_zip,
    p.geometry
FROM parcels p
JOIN properties pr
    ON p.strap = pr.strap;