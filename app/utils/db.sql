CREATE TABLE URLs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  short_url VARCHAR(20) UNIQUE NOT NULL,
  original_url TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  click_count INTEGER DEFAULT 0
);

CREATE TABLE Analytics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  url_id UUID REFERENCES URLs(id) ON DELETE CASCADE,
  clicked_at TIMESTAMPTZ DEFAULT NOW(),
  device_type VARCHAR(100),
  os VARCHAR(30),
  browser VARCHAR(40)
);

-- Initial Table Design
-- CREATE TABLE URLS (
--   id UUID PRIMARY KEY,
--   short_url VARCHAR(20) UNIQUE NOT NULL,
--   original_url TEXT NOT NULL,
--   created_at TIMESTAMPTZ,
--   click_count INTEGER,
--   device_type VARCHAR(100),
--   os VARCHAR(30),
--   browser VARCHAR(40)
-- ); 




