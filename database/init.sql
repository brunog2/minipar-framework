CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS compilation_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_code TEXT NOT NULL,
  target_variability VARCHAR(32) NOT NULL,
  execution_mode VARCHAR(32) NOT NULL,
  status VARCHAR(16) NOT NULL,
  output TEXT,
  error TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_compilation_history_created_at
  ON compilation_history (created_at DESC);
