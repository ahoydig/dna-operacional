-- DNA Operacional — Migration v0.1.0 (Supabase backend)
-- Uso: rodar 1 vez no SQL Editor do Supabase do user.
-- Cria as 7 tabelas + indexes + triggers de updated_at.

-- =====================================================
-- competitors
-- =====================================================
CREATE TABLE IF NOT EXISTS competitors (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  instagram_username TEXT NOT NULL UNIQUE,
  instagram_profile_url TEXT NOT NULL,
  followers_count INT,
  foto TEXT,
  nicho TEXT,
  sub_nicho TEXT,
  avg_engagement_coefficient NUMERIC(10, 4),
  posts_analyzed_count INT DEFAULT 0,
  last_avg_update TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_competitors_nicho ON competitors(nicho);
CREATE INDEX IF NOT EXISTS idx_competitors_username ON competitors(instagram_username);

-- =====================================================
-- competitor_posts
-- =====================================================
CREATE TABLE IF NOT EXISTS competitor_posts (
  id BIGSERIAL PRIMARY KEY,
  competitor_id BIGINT NOT NULL REFERENCES competitors(id) ON DELETE CASCADE,
  platform TEXT NOT NULL CHECK (platform IN ('instagram', 'tiktok', 'youtube')),
  post_url TEXT NOT NULL,
  post_code TEXT NOT NULL,
  published_at TIMESTAMPTZ,
  likes INT,
  comments INT,
  video_views INT,
  transcription TEXT,
  hook TEXT,
  hook_visual TEXT,
  angulo TEXT,
  pilar TEXT,
  categoria TEXT,
  formato TEXT,
  engagement_score NUMERIC(10, 4),
  UNIQUE (competitor_id, post_code)
);

CREATE INDEX IF NOT EXISTS idx_posts_competitor ON competitor_posts(competitor_id);
CREATE INDEX IF NOT EXISTS idx_posts_platform ON competitor_posts(platform);

-- =====================================================
-- content_pipeline
-- =====================================================
CREATE TABLE IF NOT EXISTS content_pipeline (
  id BIGSERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'Ideia' CHECK (status IN ('Ideia','Pesquisado','Roteirizado','Gravado','Publicado','Arquivado')),
  source TEXT,
  source_url TEXT,
  topic TEXT,
  angulo TEXT,
  hook_suggestion TEXT,
  motivo_video TEXT,
  research_brief TEXT,
  format TEXT,
  archetype TEXT,
  platform TEXT,
  variant_of BIGINT REFERENCES content_pipeline(id),
  published_content_id BIGINT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_pipeline_status ON content_pipeline(status);

-- =====================================================
-- my_content (estrutura herdada Rodada 1)
-- =====================================================
CREATE TABLE IF NOT EXISTS my_content (
  id BIGSERIAL PRIMARY KEY,
  post_url TEXT NOT NULL UNIQUE,
  post_code TEXT,
  platform TEXT NOT NULL,
  published_at TIMESTAMPTZ,
  likes INT,
  comments INT,
  saves INT,
  shares INT,
  video_views INT,
  reach INT,
  impressions INT,
  hook TEXT,
  topic TEXT,
  pilar TEXT,
  formato TEXT,
  archetype TEXT,
  transcript TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_my_content_published ON my_content(published_at);
CREATE INDEX IF NOT EXISTS idx_my_content_platform ON my_content(platform);

-- =====================================================
-- ad_library (estrutura herdada Rodada 1)
-- =====================================================
CREATE TABLE IF NOT EXISTS ad_library (
  id BIGSERIAL PRIMARY KEY,
  competitor_id BIGINT REFERENCES competitors(id),
  ad_id_meta TEXT NOT NULL,
  headline TEXT,
  primary_text TEXT,
  cta TEXT,
  image_url TEXT,
  video_url TEXT,
  landing_page_url TEXT,
  started_at TIMESTAMPTZ,
  last_seen_at TIMESTAMPTZ,
  running_days INT,
  countries TEXT[],
  ad_format TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (ad_id_meta)
);

CREATE INDEX IF NOT EXISTS idx_ads_competitor ON ad_library(competitor_id);

-- =====================================================
-- adaptive_models (NOVO v0.1.0)
-- =====================================================
CREATE TABLE IF NOT EXISTS adaptive_models (
  id BIGSERIAL PRIMARY KEY,
  source_video_url TEXT NOT NULL,
  hook_visual TEXT NOT NULL,
  hook_falado TEXT NOT NULL,
  structure_json JSONB NOT NULL,
  arquetipo TEXT,
  formato TEXT,
  duracao INT,
  transcript TEXT,
  frame_analysis_json JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =====================================================
-- generated_scripts (NOVO v0.1.0)
-- =====================================================
CREATE TABLE IF NOT EXISTS generated_scripts (
  id BIGSERIAL PRIMARY KEY,
  adaptive_model_id BIGINT NOT NULL REFERENCES adaptive_models(id) ON DELETE CASCADE,
  tema TEXT NOT NULL,
  hook TEXT NOT NULL,
  body TEXT NOT NULL,
  cta TEXT,
  formato TEXT,
  duracao_target INT,
  voz_handle TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_scripts_model ON generated_scripts(adaptive_model_id);

-- =====================================================
-- Trigger de updated_at automático
-- =====================================================
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
DECLARE t text;
BEGIN
  FOR t IN SELECT unnest(ARRAY['competitors','content_pipeline','my_content','ad_library']) LOOP
    EXECUTE format('DROP TRIGGER IF EXISTS trg_set_updated_at ON %I;', t);
    EXECUTE format('CREATE TRIGGER trg_set_updated_at BEFORE UPDATE ON %I FOR EACH ROW EXECUTE FUNCTION set_updated_at();', t);
  END LOOP;
END;
$$;
