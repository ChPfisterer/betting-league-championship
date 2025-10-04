-- Enable required PostgreSQL extensions
-- This script should be run after database creation

-- UUID extension for generating UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- pg_stat_statements for query performance monitoring
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- pg_trgm for text search and similarity
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- btree_gin for additional indexing capabilities
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- TimescaleDB extension (if needed for time-series data)
-- CREATE EXTENSION IF NOT EXISTS "timescaledb";
