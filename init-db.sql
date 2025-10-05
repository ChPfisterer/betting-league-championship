-- Database initialization script for development
-- This script sets up the basic databases and extensions

-- Create main application database
-- (POSTGRES_DB=betting_championship is handled by environment variable)

-- Create Keycloak database
CREATE DATABASE keycloak;

-- Connect to the main database
\c betting_championship;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable pgcrypto extension for password hashing
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create a development schema
CREATE SCHEMA IF NOT EXISTS dev;

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON SCHEMA dev TO postgres;

-- Connect to Keycloak database and set it up
\c keycloak;

-- Enable UUID extension for Keycloak
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA public TO postgres;

-- Back to main database
\c betting_championship;

-- Log the initialization
SELECT 'Databases initialized successfully for development (betting_championship + keycloak)' AS status;