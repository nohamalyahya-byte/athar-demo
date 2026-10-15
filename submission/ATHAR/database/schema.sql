-- ATHAR demo database schema (SQLite). All data is synthetic / illustrative.
PRAGMA foreign_keys = ON;
CREATE TABLE departments (code TEXT PRIMARY KEY, name_ar TEXT NOT NULL, name_en TEXT NOT NULL);
CREATE TABLE places (code TEXT PRIMARY KEY, name_ar TEXT NOT NULL, name_en TEXT NOT NULL);
CREATE TABLE signal_types (key TEXT PRIMARY KEY, weight INTEGER NOT NULL, name_ar TEXT NOT NULL, name_en TEXT NOT NULL, source_ar TEXT NOT NULL, source_en TEXT NOT NULL);
CREATE TABLE thresholds (key TEXT PRIMARY KEY, value INTEGER NOT NULL, description_ar TEXT);
CREATE TABLE cases (
  id TEXT PRIMARY KEY, name_ar TEXT NOT NULL, name_en TEXT NOT NULL, age INTEGER NOT NULL,
  dept_code TEXT NOT NULL REFERENCES departments(code),
  status TEXT NOT NULL CHECK (status IN ('review','contacting','processing','resolved','escalated','closed_no_action')),
  interactive INTEGER NOT NULL DEFAULT 0,
  consent_status TEXT NOT NULL CHECK (consent_status IN ('none','granted','denied','withdrawn')),
  consent_at TEXT, consent_last TEXT,
  instant_state TEXT CHECK (instant_state IN ('open','ended','closed')), instant_at TEXT, instant_reason_ar TEXT, instant_reason_en TEXT
);
CREATE TABLE case_signals (
  id INTEGER PRIMARY KEY AUTOINCREMENT, case_id TEXT NOT NULL REFERENCES cases(id), signal_key TEXT NOT NULL REFERENCES signal_types(key),
  weight INTEGER NOT NULL, state TEXT NOT NULL CHECK (state IN ('active','hist')), source TEXT NOT NULL CHECK (source IN ('sys','loc')),
  evidence_id TEXT NOT NULL, path_checked INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE journey_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT, case_id TEXT NOT NULL REFERENCES cases(id), what_ar TEXT NOT NULL, what_en TEXT NOT NULL,
  start_at TEXT, updated_at TEXT, place_code TEXT REFERENCES places(code), place_source TEXT NOT NULL CHECK (place_source IN ('sys','loc')),
  source_ar TEXT, source_en TEXT, status TEXT NOT NULL CHECK (status IN ('on','off','chk')), note_ar TEXT, note_en TEXT
);
CREATE TABLE case_updates (
  case_id TEXT PRIMARY KEY REFERENCES cases(id),
  contact TEXT NOT NULL CHECK (contact IN ('none','ok','noans','later')),
  verify TEXT NOT NULL CHECK (verify IN ('open','need','noneed','insuf')),
  action_desc TEXT, owner TEXT, assignee TEXT, follow_up_date TEXT, result_desc TEXT, result_how TEXT
);
CREATE TABLE follow_up_log (id INTEGER PRIMARY KEY AUTOINCREMENT, case_id TEXT NOT NULL REFERENCES cases(id), at TEXT NOT NULL, kind TEXT NOT NULL, value_ar TEXT, value_en TEXT);
CREATE TABLE location_pings (id INTEGER PRIMARY KEY AUTOINCREMENT, case_id TEXT NOT NULL REFERENCES cases(id), seq INTEGER NOT NULL, place_code TEXT NOT NULL REFERENCES places(code));
-- Contact priority score = sum of weights of active, qualifying, non-duplicate signals (see README).
CREATE VIEW v_case_scores AS
  SELECT c.id AS case_id, c.status, COALESCE(SUM(CASE WHEN s.state='active' AND (s.source='sys' OR c.consent_status='granted') THEN s.weight END),0) AS score
  FROM cases c LEFT JOIN case_signals s ON s.case_id=c.id GROUP BY c.id;
