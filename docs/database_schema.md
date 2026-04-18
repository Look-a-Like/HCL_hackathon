# Database Schema — Agentic Travel Assistant

This schema is designed to support high-scale travel planning, multi-agent orchestration tracking, and AI-driven personalization.

## 1. User & Profile Management

Handles authentication and long-term personalization priors for the AI.

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_profiles (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    home_city VARCHAR(100),
    preferred_currency VARCHAR(3) DEFAULT 'INR',
    -- AI Personalization: Stored as JSONB for flexibility in interest tags
    interests JSONB DEFAULT '[]',
    travel_style VARCHAR(50), -- e.g., 'Budget', 'Luxury', 'Adventure'
    last_active TIMESTAMP WITH TIME ZONE
);
```

## 2. Global Travel Knowledge Base

Relational structure to replace the current `data/*.json` mock files.

```sql
CREATE TABLE destinations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    country VARCHAR(100) DEFAULT 'India',
    description TEXT,
    location_type VARCHAR(50), -- beach, mountain, city
    avg_daily_cost_inr DECIMAL(10, 2),
    best_season_start MONTH,
    best_season_end MONTH,
    keywords JSONB DEFAULT '[]' -- For AI matching
);

CREATE TABLE attractions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    destination_id UUID REFERENCES destinations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50), -- historical, nature, food
    estimated_cost_inr DECIMAL(10, 2),
    recommended_duration_mins INTEGER
);
```

## 3. Travel History & AI Generated Plans

Stores the output of the LangGraph workflow, linked to specific users.

```sql
CREATE TABLE travel_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    destination_id UUID REFERENCES destinations(id),
    title VARCHAR(255),
    start_date DATE,
    end_date DATE,
    total_budget DECIMAL(12, 2),
    -- Stores the full finalized state for quick retrieval
    final_itinerary_json JSONB,
    status VARCHAR(20) DEFAULT 'draft', -- draft, confirmed, completed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Versioning for plan refinements
CREATE TABLE plan_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_id UUID REFERENCES travel_plans(id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL,
    user_prompt_refinement TEXT, -- What the user asked to change
    itinerary_snapshot JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## 4. AI/ML Operational Data (The "Smoothness" Layer)

Critical for monitoring agent health, optimizing costs, and improving the model.

```sql
-- Tracks every step of the LangGraph execution
CREATE TABLE agent_execution_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_id UUID REFERENCES travel_plans(id) ON DELETE CASCADE,
    agent_name VARCHAR(50) NOT NULL, -- planner, budget, itinerary, etc.
    model_used VARCHAR(100), -- e.g., claude-3-5-sonnet
    prompt_tokens INTEGER,
    completion_tokens INTEGER,
    latency_ms INTEGER,
    status VARCHAR(20), -- success, retry, failure
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- For Reinforcement Learning from Human Feedback (RLHF)
CREATE TABLE plan_feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_id UUID REFERENCES travel_plans(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    feedback_text TEXT,
    -- Which specific parts they liked/disliked
    liked_items JSONB,
    disliked_items JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## 5. Indexes for Performance

```sql
CREATE INDEX idx_dest_name ON destinations(name);
CREATE INDEX idx_user_plans ON travel_plans(user_id);
CREATE INDEX idx_agent_plan_id ON agent_execution_logs(plan_id);
```
