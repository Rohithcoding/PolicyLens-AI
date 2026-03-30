# 🏗️ PolicyLens AI Architecture

## System Overview

PolicyLens AI is a multi-agent system designed to analyze government policies and predict their impacts using synthetic population modeling.

## Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   AI Agents     │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (Python)      │
│                 │    │                 │    │                 │
│ • UI Components │    │ • REST Endpoints│    │ • Policy Agent  │
│ • State Mgmt    │    │ • Data Models   │    │ • Simulation    │
│ • Charts/Viz    │    │ • Validation    │    │ • Impact Pred.  │
│ • Forms         │    │ • Error Handling│    │ • Sentiment     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Browser       │    │   PostgreSQL    │    │   External APIs │
│                 │    │                 │    │                 │
│ • React Runtime │    │ • Policy Data   │    │ • OpenAI GPT    │
│ • Tailwind CSS  │    │ • User Sessions │    │ • Anthropic     │
│ • Axios Client  │    │ • Results Cache │    │ • TextBlob NLP  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Data Flow

### 1. Policy Input Flow
```
User Input → Frontend Validation → API Endpoint → Policy Understanding Agent
                                                            ↓
Structured Policy Data ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

### 2. Analysis Pipeline
```
Policy Text → Policy Agent → Simulation Agent → Impact Agent → Sentiment Agent
     ↓              ↓              ↓             ↓            ↓
  Structured    Synthetic      Economic      Social      Public
  Analysis     Population     Impact        Impact      Sentiment
     ↓              ↓              ↓             ↓            ↓
     └─────────────┴──────────────┴─────────────┴────────────┘
                           ↓
                    Results Dashboard
```

### 3. What-If Simulation Flow
```
User Adjustments → Parameter Validation → Modified Policy Analysis
                                               ↓
                                    New Impact Predictions
                                               ↓
                                    Updated Results Display
```

## Component Architecture

### Frontend (Next.js)

#### Pages Structure
```
app/
├── layout.tsx          # Root layout with providers
├── page.tsx           # Main dashboard
├── globals.css        # Global styles
└── loading.tsx        # Loading states
```

#### Components Structure
```
components/
├── PolicyInput.tsx        # Policy text input form
├── SimulationResults.tsx  # Results dashboard
├── WhatIfSimulation.tsx   # What-if controls
├── Header.tsx            # Navigation header
├── Footer.tsx            # Footer component
└── LoadingSpinner.tsx    # Loading animation
```

#### State Management
- React hooks (useState, useEffect)
- Form handling with react-hook-form
- Toast notifications with react-hot-toast
- API client with axios

### Backend (FastAPI)

#### API Routes
```
/api/
├── policy/
│   ├── POST /analyze          # Main policy analysis
│   ├── POST /what-if          # What-if simulation
│   └── GET /sectors          # Available sectors
└── simulation/
    ├── GET /population/default    # Default population
    ├── POST /population/custom    # Custom population
    └── GET /demographics          # Demographic options
```

#### Data Models
```python
PolicyInput          # User policy input
PolicyAnalysis       # Structured policy data
SyntheticPopulation  # Virtual population data
EconomicImpact       # Economic predictions
SocialImpact         # Social predictions
SentimentResult      # Sentiment analysis
SimulationResult     # Complete analysis result
```

### AI Agents

#### 1. Policy Understanding Agent
```python
class PolicyUnderstandingAgent:
    - analyze_policy()          # Main analysis function
    - _openai_analysis()        # OpenAI GPT analysis
    - _anthropic_analysis()     # Claude analysis
    - _rule_based_analysis()    # Fallback rule-based
    - apply_adjustments()       # What-if modifications
```

#### 2. Simulation Agent
```python
class SimulationAgent:
    - create_population()           # Generate synthetic pop
    - create_default_population()   # Default 1M population
    - create_custom_population()    # Custom parameters
    - generate_individual_profiles() # Detailed profiles
    - calculate_vulnerability()     # Vulnerability index
```

#### 3. Impact Prediction Agent
```python
class ImpactPredictionAgent:
    - predict_impacts()           # Main prediction function
    - _calculate_economic_impact() # Economic metrics
    - _calculate_social_impact()   # Social metrics
    - assess_risks()              # Risk assessment
    - generate_recommendations()  # Policy recommendations
```

#### 4. Sentiment Analysis Agent
```python
class SentimentAgent:
    - analyze_sentiment()         # Main sentiment analysis
    - analyze_stakeholder_sentiment() # Per-group analysis
    - predict_sentiment_change()   # What-if sentiment
    - _analyze_sentiment_by_keywords() # Keyword-based fallback
```

## Database Schema

### Core Tables
```sql
-- Policy analyses
CREATE TABLE policy_analyses (
    id UUID PRIMARY KEY,
    policy_text TEXT,
    analysis_result JSONB,
    created_at TIMESTAMP,
    user_session VARCHAR
);

-- Simulation results
CREATE TABLE simulation_results (
    id UUID PRIMARY KEY,
    policy_id UUID REFERENCES policy_analyses(id),
    economic_impact JSONB,
    social_impact JSONB,
    sentiment_result JSONB,
    confidence_score FLOAT
);

-- User sessions
CREATE TABLE user_sessions (
    session_id VARCHAR PRIMARY KEY,
    created_at TIMESTAMP,
    last_activity TIMESTAMP,
    analysis_count INTEGER
);
```

## Performance Considerations

### Frontend Optimization
- Code splitting with Next.js dynamic imports
- Image optimization with next/image
- Component memoization with React.memo
- Debounced form inputs

### Backend Optimization
- Async/await for non-blocking operations
- Connection pooling for database
- Response caching with TTL
- Rate limiting for API endpoints

### AI Agent Optimization
- Parallel agent execution where possible
- Fallback mechanisms for API failures
- Response caching for similar policies
- Batch processing for population simulation

## Security Considerations

### Frontend Security
- Input sanitization and validation
- XSS prevention with React's built-in protection
- CSRF protection with same-site cookies
- Content Security Policy headers

### Backend Security
- API key encryption and rotation
- Input validation with Pydantic models
- SQL injection prevention with ORMs
- Rate limiting and DDoS protection

### Data Privacy
- No PII collection or storage
- Anonymous session tracking
- Data retention policies
- GDPR compliance considerations

## Deployment Architecture

### Development Environment
```
Local Machine:
├── Frontend (npm run dev)     :3000
├── Backend (python main.py)  :8000
└── Database (PostgreSQL)     :5432
```

### Production Environment
```
Cloud Infrastructure:
├── Frontend (Vercel/Netlify)   CDN
├── Backend (Railway/Heroku)    Container
├── Database (PostgreSQL)       Managed DB
└── Monitoring (Logs/Metrics)   Observability
```

## Monitoring & Logging

### Frontend Monitoring
- React Error Boundaries
- Performance metrics with Web Vitals
- User interaction tracking
- Error reporting to backend

### Backend Monitoring
- Structured logging with Python logging
- API response time tracking
- Error rate monitoring
- Resource usage metrics

### AI Agent Monitoring
- API call success rates
- Response time distributions
- Confidence score distributions
- Fallback activation rates

## Scaling Strategy

### Horizontal Scaling
- Stateless API design
- Load balancing for backend
- CDN for frontend assets
- Database read replicas

### Vertical Scaling
- Memory optimization for population simulation
- CPU allocation for AI processing
- Storage scaling for result data
- Network bandwidth for API calls

## Future Architecture Enhancements

### Planned Improvements
1. **Microservices Architecture**: Split agents into separate services
2. **Event-Driven Processing**: Use message queues for async processing
3. **Machine Learning Pipeline**: Add model training and versioning
4. **Real-time Collaboration**: Multi-user policy analysis sessions
5. **Advanced Visualization**: 3D charts and interactive maps

### Technology Roadmap
- **Phase 1**: Current monolithic architecture (MVP)
- **Phase 2**: Microservices with message queues
- **Phase 3**: ML pipeline with model management
- **Phase 4**: Real-time collaboration features
- **Phase 5**: Advanced analytics and AI/ML
