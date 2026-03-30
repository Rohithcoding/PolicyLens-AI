export interface PolicyInput {
  text: string
  title?: string
  adjustments?: Record<string, number>
}

export interface PolicyAnalysis {
  sector: string
  key_changes: string[]
  stakeholders: string[]
  budget_impact?: number
  implementation_timeframe?: string
  confidence_score: number
}

export interface SyntheticPopulation {
  total_population: number
  demographics: Record<string, number>
  income_distribution: Record<string, number>
  employment_data: Record<string, number>
  regional_data: Record<string, Record<string, any>>
}

export interface EconomicImpact {
  gdp_change: number
  inflation_impact: number
  employment_change: number
  budget_impact: number
  sector_impacts: Record<string, number>
}

export interface SocialImpact {
  poverty_reduction: number
  education_improvement: number
  healthcare_access: number
  social_inequality: number
}

export interface SentimentResult {
  overall_sentiment: string
  sentiment_score: number
  key_concerns: string[]
  public_support_percentage: number
}

export interface SimulationResult {
  policy_analysis: PolicyAnalysis
  economic_impact: EconomicImpact
  social_impact: SocialImpact
  sentiment: SentimentResult
  risk_assessment: Record<string, string>
  recommendations: string[]
  confidence_score: number
}

export interface WhatIfAdjustment {
  tax_rate?: number
  subsidy_increase?: number
  budget_increase?: number
  implementation_speed?: number
}
