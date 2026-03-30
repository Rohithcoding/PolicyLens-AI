# 📚 PolicyLens AI API Documentation

## Base URL

```
Development: http://localhost:8000
Production: https://api.policylens.ai
```

## Authentication

Currently no authentication required (development mode). Future versions will include API key authentication.

## Response Format

All API responses follow this structure:

```json
{
  "data": {}, // Response data
  "message": "string", // Success/error message
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Error Handling

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {}
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Endpoints

### 🏛️ Policy Analysis

#### Analyze Policy
```http
POST /api/policy/analyze
```

Analyzes policy text and returns comprehensive simulation results.

**Request Body:**
```json
{
  "text": "The government proposes to increase agricultural subsidies...",
  "title": "Agricultural Reform Bill (optional)",
  "sector": "agriculture (optional)"
}
```

**Response:**
```json
{
  "policy_analysis": {
    "sector": "agriculture",
    "key_changes": ["Increased subsidies by 20%", "Low-interest loans"],
    "stakeholders": ["farmers", "government", "consumers"],
    "budget_impact": 500.0,
    "implementation_timeframe": "18 months",
    "confidence_score": 0.85
  },
  "economic_impact": {
    "gdp_change": 0.08,
    "inflation_impact": 0.02,
    "employment_change": 0.05,
    "budget_impact": 500.0,
    "sector_impacts": {
      "agriculture": 0.12,
      "manufacturing": 0.03,
      "services": 0.02
    }
  },
  "social_impact": {
    "poverty_reduction": 0.15,
    "education_improvement": 0.02,
    "healthcare_access": 0.03,
    "social_inequality": -0.08
  },
  "sentiment": {
    "overall_sentiment": "Positive",
    "sentiment_score": 0.65,
    "key_concerns": ["Implementation complexity", "Budget constraints"],
    "public_support_percentage": 72.5
  },
  "risk_assessment": {
    "budget": "Moderate budget impact within acceptable limits",
    "implementation": "Complex implementation may face delays",
    "political": "Likely to receive broad political support",
    "economic": "Minimal economic disruption expected",
    "social": "Broad social acceptance likely"
  },
  "recommendations": [
    "Monitor implementation progress quarterly",
    "Provide training programs for farmers",
    "Establish clear metrics for success measurement"
  ],
  "confidence_score": 0.82
}
```

#### What-If Simulation
```http
POST /api/policy/what-if
```

Runs what-if simulation with policy adjustments.

**Request Body:**
```json
{
  "policy_text": "The government proposes to increase agricultural subsidies...",
  "adjustments": {
    "tax_rate": 0.1,        // +10% tax change
    "subsidy_increase": 0.2, // +20% subsidy
    "budget_increase": 0.15, // +15% budget
    "implementation_speed": 0.1 // +10% faster implementation
  },
  "target_demographic": "rural (optional)"
}
```

**Response:** Same structure as policy analysis with adjusted results.

#### Get Policy Sectors
```http
GET /api/policy/sectors
```

Returns list of available policy sectors.

**Response:**
```json
{
  "sectors": [
    "agriculture",
    "taxation", 
    "healthcare",
    "education",
    "infrastructure",
    "environment",
    "social_welfare",
    "economy"
  ]
}
```

### 🎭 Simulation

#### Get Default Population
```http
GET /api/simulation/population/default
```

Returns default synthetic population data.

**Response:**
```json
{
  "total_population": 1000000,
  "demographics": {
    "18-25": 200000,
    "26-35": 250000,
    "36-50": 250000,
    "51-65": 200000,
    "65+": 100000
  },
  "income_distribution": {
    "low": 400000,
    "middle": 450000,
    "high": 150000
  },
  "employment_data": {
    "agriculture": 162500,
    "manufacturing": 130000,
    "services": 227500,
    "technology": 65000,
    "government": 65000,
    "overall_employment_rate": 0.65,
    "unemployment_rate": 0.35
  },
  "regional_data": {
    "urban": {
      "population": 350000,
      "avg_income": 65000,
      "education_level": "higher",
      "main_sectors": ["technology", "services", "manufacturing"],
      "infrastructure_quality": 0.8
    },
    "rural": {
      "population": 500000,
      "avg_income": 35000,
      "education_level": "moderate", 
      "main_sectors": ["agriculture", "manufacturing", "services"],
      "infrastructure_quality": 0.4
    },
    "suburban": {
      "population": 150000,
      "avg_income": 50000,
      "education_level": "moderate",
      "main_sectors": ["services", "manufacturing", "technology"],
      "infrastructure_quality": 0.6
    }
  }
}
```

#### Create Custom Population
```http
POST /api/simulation/population/custom
```

Creates custom population with specified parameters.

**Request Body:**
```json
{
  "total_population": 2000000,
  "urban_ratio": 0.4,
  "median_income": 60000
}
```

**Response:** Same structure as default population with custom values.

#### Get Demographic Options
```http
GET /api/simulation/demographics
```

Returns available demographic options for simulation.

**Response:**
```json
{
  "age_groups": ["18-25", "26-35", "36-50", "51-65", "65+"],
  "income_levels": ["low", "middle", "high"],
  "regions": ["urban", "rural", "suburban"],
  "employment_sectors": ["agriculture", "manufacturing", "services", "technology"]
}
```

### 🔧 System

#### Health Check
```http
GET /health
```

Returns system health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00Z",
  "services": {
    "database": "healthy",
    "ai_agents": "healthy",
    "external_apis": "healthy"
  }
}
```

#### Root Endpoint
```http
GET /
```

Returns API information.

**Response:**
```json
{
  "message": "PolicyLens AI API is running",
  "version": "1.0.0",
  "documentation": "/docs"
}
```

## Data Models

### PolicyInput
```typescript
interface PolicyInput {
  text: string;              // Policy text content (required)
  title?: string;            // Policy title (optional)
  sector?: string;           // Policy sector (optional)
  adjustments?: {            // For what-if scenarios
    tax_rate?: number;
    subsidy_increase?: number;
    budget_increase?: number;
    implementation_speed?: number;
  };
  target_demographic?: string; // Target demographic (optional)
}
```

### PolicyAnalysis
```typescript
interface PolicyAnalysis {
  sector: string;                    // Policy sector
  key_changes: string[];             // Main policy changes
  stakeholders: string[];            // Affected stakeholders
  budget_impact?: number;            // Budget impact in millions
  implementation_timeframe?: string; // Implementation timeline
  confidence_score: number;          // Analysis confidence (0-1)
}
```

### EconomicImpact
```typescript
interface EconomicImpact {
  gdp_change: number;           // GDP change percentage
  inflation_impact: number;      // Inflation impact percentage
  employment_change: number;     // Employment change percentage
  budget_impact: number;        // Budget impact in millions
  sector_impacts: {             // Sector-specific impacts
    [sector: string]: number;
  };
}
```

### SocialImpact
```typescript
interface SocialImpact {
  poverty_reduction: number;     // Poverty reduction percentage
  education_improvement: number; // Education improvement percentage
  healthcare_access: number;     // Healthcare access improvement
  social_inequality: number;     // Social inequality change
}
```

### SentimentResult
```typescript
interface SentimentResult {
  overall_sentiment: string;           // Positive/Negative/Neutral
  sentiment_score: number;             // Sentiment score (-1 to 1)
  key_concerns: string[];              // Main concerns
  public_support_percentage: number;   // Public support percentage
}
```

## Rate Limits

- **Development**: No rate limiting
- **Production**: 100 requests per minute per IP
- **Premium**: 1000 requests per minute per API key

## Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `VALIDATION_ERROR` | Invalid input data | 400 |
| `POLICY_TOO_LONG` | Policy text exceeds limit | 400 |
| `AI_SERVICE_ERROR` | External AI service failure | 502 |
| `SIMULATION_ERROR` | Population simulation failure | 500 |
| `RATE_LIMIT_EXCEEDED` | Too many requests | 429 |
| `INTERNAL_ERROR` | Internal server error | 500 |

## SDK Examples

### Python
```python
import requests

# Analyze policy
response = requests.post('http://localhost:8000/api/policy/analyze', json={
    'text': 'The government proposes to increase agricultural subsidies...'
})

result = response.json()
print(f"GDP Impact: {result['economic_impact']['gdp_change']:.2%}")
```

### JavaScript
```javascript
// Analyze policy
const response = await fetch('http://localhost:8000/api/policy/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: 'The government proposes to increase agricultural subsidies...'
  })
});

const result = await response.json();
console.log(`GDP Impact: ${(result.economic_impact.gdp_change * 100).toFixed(1)}%`);
```

### cURL
```bash
# Analyze policy
curl -X POST http://localhost:8000/api/policy/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The government proposes to increase agricultural subsidies by 20%..."
  }'
```

## WebSocket API (Future)

Real-time policy analysis updates:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/analysis');

ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  console.log('Analysis progress:', update);
};
```

## Changelog

### v1.0.0 (Current)
- Basic policy analysis
- What-if simulation
- Synthetic population modeling
- Sentiment analysis

### Planned v1.1.0
- WebSocket real-time updates
- Batch analysis
- Export functionality
- Advanced filtering

### Planned v2.0.0
- Multi-user collaboration
- Model versioning
- Custom agent training
- Advanced analytics
