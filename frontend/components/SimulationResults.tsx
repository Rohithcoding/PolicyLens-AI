'use client'

import { SimulationResult } from '@/types/policy'
import { 
  TrendingUp, 
  TrendingDown, 
  Users, 
  DollarSign, 
  AlertTriangle, 
  CheckCircle,
  BarChart3,
  PieChart,
  Heart,
  GraduationCap
} from 'lucide-react'

interface SimulationResultsProps {
  result: SimulationResult
}

export function SimulationResults({ result }: SimulationResultsProps) {
  const formatPercentage = (value: number) => `${(value * 100).toFixed(1)}%`
  const formatCurrency = (value: number) => `$${Math.abs(value).toFixed(1)}M`
  
  const getSentimentColor = (sentiment: string) => {
    switch (sentiment.toLowerCase()) {
      case 'positive': return 'text-success-600 bg-success-50'
      case 'negative': return 'text-danger-600 bg-danger-50'
      default: return 'text-gray-600 bg-gray-50'
    }
  }

  const getImpactColor = (value: number) => {
    if (value > 0.01) return 'text-success-600'
    if (value < -0.01) return 'text-danger-600'
    return 'text-gray-600'
  }

  const getImpactIcon = (value: number) => {
    if (value > 0.01) return <TrendingUp className="w-4 h-4" />
    if (value < -0.01) return <TrendingDown className="w-4 h-4" />
    return <div className="w-4 h-4" />
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Policy Analysis Results</h2>
        <div className="flex items-center justify-center space-x-4">
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${getSentimentColor(result.sentiment.overall_sentiment)}`}>
            {result.sentiment.overall_sentiment} Sentiment
          </span>
          <span className="text-gray-500">|</span>
          <span className="text-sm text-gray-600">
            Confidence: {(result.confidence_score * 100).toFixed(0)}%
          </span>
        </div>
      </div>

      {/* Policy Overview */}
      <div className="card">
        <h3 className="text-xl font-semibold mb-4 flex items-center">
          <BarChart3 className="w-6 h-6 mr-2 text-primary-600" />
          Policy Overview
        </h3>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Sector</h4>
            <p className="text-gray-600 capitalize">{result.policy_analysis.sector.replace('_', ' ')}</p>
          </div>
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Implementation Timeframe</h4>
            <p className="text-gray-600">{result.policy_analysis.implementation_timeframe || 'Not specified'}</p>
          </div>
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Key Changes</h4>
            <ul className="space-y-1">
              {result.policy_analysis.key_changes.map((change, index) => (
                <li key={index} className="text-gray-600 text-sm flex items-start">
                  <span className="w-2 h-2 bg-primary-400 rounded-full mt-1.5 mr-2 flex-shrink-0" />
                  {change}
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Affected Stakeholders</h4>
            <div className="flex flex-wrap gap-2">
              {result.policy_analysis.stakeholders.map((stakeholder, index) => (
                <span key={index} className="px-2 py-1 bg-gray-100 text-gray-700 text-sm rounded-md">
                  {stakeholder.replace('_', ' ')}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Economic Impact */}
      <div className="card">
        <h3 className="text-xl font-semibold mb-4 flex items-center">
          <DollarSign className="w-6 h-6 mr-2 text-success-600" />
          Economic Impact
        </h3>
        <div className="grid md:grid-cols-4 gap-4 mb-6">
          <div className="metric-card">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-600">GDP Change</span>
              <div className={getImpactColor(result.economic_impact.gdp_change)}>
                {getImpactIcon(result.economic_impact.gdp_change)}
              </div>
            </div>
            <div className={`metric-value ${getImpactColor(result.economic_impact.gdp_change)}`}>
              {formatPercentage(result.economic_impact.gdp_change)}
            </div>
          </div>
          
          <div className="metric-card">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-600">Inflation Impact</span>
              <div className={getImpactColor(result.economic_impact.inflation_impact)}>
                {getImpactIcon(result.economic_impact.inflation_impact)}
              </div>
            </div>
            <div className={`metric-value ${getImpactColor(result.economic_impact.inflation_impact)}`}>
              {formatPercentage(result.economic_impact.inflation_impact)}
            </div>
          </div>
          
          <div className="metric-card">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-600">Employment</span>
              <div className={getImpactColor(result.economic_impact.employment_change)}>
                {getImpactIcon(result.economic_impact.employment_change)}
              </div>
            </div>
            <div className={`metric-value ${getImpactColor(result.economic_impact.employment_change)}`}>
              {formatPercentage(result.economic_impact.employment_change)}
            </div>
          </div>
          
          <div className="metric-card">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-600">Budget Impact</span>
              <DollarSign className="w-4 h-4 text-gray-400" />
            </div>
            <div className="metric-value text-gray-900">
              {formatCurrency(result.economic_impact.budget_impact)}
            </div>
          </div>
        </div>

        {/* Sector Impacts */}
        <div>
          <h4 className="font-medium text-gray-900 mb-3">Sector-Specific Impacts</h4>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
            {Object.entries(result.economic_impact.sector_impacts).map(([sector, impact]) => (
              <div key={sector} className="text-center p-3 bg-gray-50 rounded-lg">
                <div className={`text-sm font-medium ${getImpactColor(impact)}`}>
                  {formatPercentage(impact)}
                </div>
                <div className="text-xs text-gray-600 capitalize mt-1">{sector}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Social Impact */}
      <div className="card">
        <h3 className="text-xl font-semibold mb-4 flex items-center">
          <Users className="w-6 h-6 mr-2 text-primary-600" />
          Social Impact
        </h3>
        <div className="grid md:grid-cols-4 gap-4">
          <div className="metric-card">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-600 flex items-center">
                <Heart className="w-4 h-4 mr-1" /> Poverty Reduction
              </span>
            </div>
            <div className="metric-value text-success-600">
              {formatPercentage(result.social_impact.poverty_reduction)}
            </div>
          </div>
          
          <div className="metric-card">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-600 flex items-center">
                <GraduationCap className="w-4 h-4 mr-1" /> Education
              </span>
            </div>
            <div className="metric-value text-success-600">
              {formatPercentage(result.social_impact.education_improvement)}
            </div>
          </div>
          
          <div className="metric-card">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-600 flex items-center">
                <Heart className="w-4 h-4 mr-1" /> Healthcare Access
              </span>
            </div>
            <div className="metric-value text-success-600">
              {formatPercentage(result.social_impact.healthcare_access)}
            </div>
          </div>
          
          <div className="metric-card">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-600">Social Inequality</span>
              <div className={getImpactColor(result.social_impact.social_inequality)}>
                {getImpactIcon(result.social_impact.social_inequality)}
              </div>
            </div>
            <div className={`metric-value ${getImpactColor(result.social_impact.social_inequality)}`}>
              {formatPercentage(result.social_impact.social_inequality)}
            </div>
          </div>
        </div>
      </div>

      {/* Public Sentiment */}
      <div className="card">
        <h3 className="text-xl font-semibold mb-4 flex items-center">
          <PieChart className="w-6 h-6 mr-2 text-warning-600" />
          Public Sentiment Analysis
        </h3>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="text-sm text-gray-600">Overall Sentiment</span>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${getSentimentColor(result.sentiment.overall_sentiment)}`}>
                {result.sentiment.overall_sentiment}
              </span>
            </div>
            <div className="flex items-center justify-between mb-4">
              <span className="text-sm text-gray-600">Sentiment Score</span>
              <span className="font-medium">{result.sentiment.sentiment_score.toFixed(2)}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Public Support</span>
              <span className="font-medium">{result.sentiment.public_support_percentage.toFixed(1)}%</span>
            </div>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Key Concerns</h4>
            <ul className="space-y-2">
              {result.sentiment.key_concerns.map((concern, index) => (
                <li key={index} className="flex items-start text-sm text-gray-600">
                  <AlertTriangle className="w-4 h-4 text-warning-500 mr-2 mt-0.5 flex-shrink-0" />
                  {concern}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Risk Assessment */}
      <div className="card">
        <h3 className="text-xl font-semibold mb-4 flex items-center">
          <AlertTriangle className="w-6 h-6 mr-2 text-danger-600" />
          Risk Assessment
        </h3>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.entries(result.risk_assessment).map(([risk, description]) => (
            <div key={risk} className="p-4 bg-gray-50 rounded-lg">
              <h4 className="font-medium text-gray-900 capitalize mb-2">{risk.replace('_', ' ')}</h4>
              <p className="text-sm text-gray-600">{description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Recommendations */}
      <div className="card">
        <h3 className="text-xl font-semibold mb-4 flex items-center">
          <CheckCircle className="w-6 h-6 mr-2 text-success-600" />
          Recommendations
        </h3>
        <div className="grid md:grid-cols-2 gap-4">
          {result.recommendations.map((recommendation, index) => (
            <div key={index} className="flex items-start space-x-3 p-4 bg-success-50 rounded-lg">
              <CheckCircle className="w-5 h-5 text-success-600 mt-0.5 flex-shrink-0" />
              <p className="text-sm text-gray-700">{recommendation}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
