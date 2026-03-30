'use client'

import { useState } from 'react'
import { SimulationResult, WhatIfAdjustment } from '@/types/policy'
import { Settings, Zap, TrendingUp, DollarSign, Clock } from 'lucide-react'

interface WhatIfSimulationProps {
  currentResult: SimulationResult
  onSimulate: (adjustments: Record<string, number>) => void
}

export function WhatIfSimulation({ currentResult, onSimulate }: WhatIfSimulationProps) {
  const [adjustments, setAdjustments] = useState<WhatIfAdjustment>({
    tax_rate: 0,
    subsidy_increase: 0,
    budget_increase: 0,
    implementation_speed: 0
  })
  
  const [isSimulating, setIsSimulating] = useState(false)

  const handleAdjustment = (key: keyof WhatIfAdjustment, value: number) => {
    setAdjustments(prev => ({
      ...prev,
      [key]: value
    }))
  }

  const handleSimulate = async () => {
    setIsSimulating(true)
    try {
      await onSimulate(adjustments as Record<string, number>)
    } finally {
      setIsSimulating(false)
    }
  }

  const resetAdjustments = () => {
    setAdjustments({
      tax_rate: 0,
      subsidy_increase: 0,
      budget_increase: 0,
      implementation_speed: 0
    })
  }

  const adjustmentControls = [
    {
      key: 'tax_rate' as keyof WhatIfAdjustment,
      label: 'Tax Rate',
      icon: <DollarSign className="w-5 h-5" />,
      min: -0.5,
      max: 0.5,
      step: 0.05,
      description: 'Adjust tax rates (-50% to +50%)',
      color: 'danger'
    },
    {
      key: 'subsidy_increase' as keyof WhatIfAdjustment,
      label: 'Subsidy Level',
      icon: <TrendingUp className="w-5 h-5" />,
      min: -0.5,
      max: 1,
      step: 0.1,
      description: 'Change subsidy amounts (-50% to +100%)',
      color: 'success'
    },
    {
      key: 'budget_increase' as keyof WhatIfAdjustment,
      label: 'Budget Allocation',
      icon: <DollarSign className="w-5 h-5" />,
      min: -0.5,
      max: 1,
      step: 0.1,
      description: 'Modify budget (-50% to +100%)',
      color: 'primary'
    },
    {
      key: 'implementation_speed' as keyof WhatIfAdjustment,
      label: 'Implementation Speed',
      icon: <Clock className="w-5 h-5" />,
      min: -0.5,
      max: 0.5,
      step: 0.1,
      description: 'Speed up or slow down implementation',
      color: 'warning'
    }
  ]

  const formatPercentage = (value: number) => {
    const percentage = value * 100
    return percentage > 0 ? `+${percentage.toFixed(0)}%` : `${percentage.toFixed(0)}%`
  }

  const getSliderColor = (color: string) => {
    switch (color) {
      case 'danger': return 'bg-danger-500'
      case 'success': return 'bg-success-500'
      case 'primary': return 'bg-primary-500'
      case 'warning': return 'bg-warning-500'
      default: return 'bg-gray-500'
    }
  }

  return (
    <div className="space-y-6 sm:space-y-8">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">What-If Simulation</h2>
        <p className="text-gray-600 text-sm sm:text-base max-w-2xl mx-auto px-4">
          Adjust policy parameters to see how changes affect outcomes. Experiment with different scenarios to find the optimal approach.
        </p>
      </div>

      {/* Current Policy Summary */}
      <div className="card-responsive bg-gradient-to-r from-primary-50 to-blue-50 border-primary-200">
        <div className="flex flex-col sm:flex-row items-center justify-between">
          <div>
            <h3 className="font-semibold text-gray-900 mb-1 text-sm sm:text-base">Current Policy</h3>
            <p className="text-sm sm:text-base text-gray-600">
              {currentResult.policy_analysis.sector.replace('_', ' ')} • 
              {currentResult.policy_analysis.implementation_timeframe}
            </p>
          </div>
          <div className="text-right mt-2 sm:mt-0">
            <div className="text-sm sm:text-base text-gray-600">Public Support</div>
            <div className="text-lg sm:text-xl font-semibold text-primary-600">
              {currentResult.sentiment.public_support_percentage.toFixed(1)}%
            </div>
          </div>
        </div>
      </div>

      {/* Adjustment Controls */}
      <div className="card">
        <div className="flex items-center mb-6">
          <Settings className="w-6 h-6 mr-2 text-primary-600" />
          <h3 className="text-xl font-semibold">Policy Adjustments</h3>
        </div>

        <div className="space-y-6">
          {adjustmentControls.map((control) => (
            <div key={control.key} className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className={`w-10 h-10 rounded-lg bg-${control.color}-100 flex items-center justify-center`}>
                    {control.icon}
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">{control.label}</h4>
                    <p className="text-sm text-gray-600">{control.description}</p>
                  </div>
                </div>
                <div className="text-right">
                  <div className={`font-semibold text-${control.color}-600`}>
                    {formatPercentage(adjustments[control.key] || 0)}
                  </div>
                </div>
              </div>

              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-500 w-12 text-right">
                  {formatPercentage(control.min)}
                </span>
                <div className="flex-1">
                  <input
                    type="range"
                    min={control.min}
                    max={control.max}
                    step={control.step}
                    value={adjustments[control.key] || 0}
                    onChange={(e) => handleAdjustment(control.key, parseFloat(e.target.value))}
                    className={`w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider-${control.color}`}
                    style={{
                      background: `linear-gradient(to right, rgb(59 130 246) 0%, rgb(59 130 246) ${((adjustments[control.key] || 0 - control.min) / (control.max - control.min)) * 100}%, rgb(229 231 235) ${((adjustments[control.key] || 0 - control.min) / (control.max - control.min)) * 100}%, rgb(229 231 235) 100%)`
                    }}
                  />
                </div>
                <span className="text-sm text-gray-500 w-12">
                  {formatPercentage(control.max)}
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* Action Buttons */}
        <div className="flex justify-center space-x-4 mt-8">
          <button
            onClick={resetAdjustments}
            className="btn-secondary"
            disabled={isSimulating}
          >
            Reset to Default
          </button>
          <button
            onClick={handleSimulate}
            disabled={isSimulating}
            className="btn-primary px-8 flex items-center space-x-2"
          >
            {isSimulating ? (
              <>
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>Simulating...</span>
              </>
            ) : (
              <>
                <Zap className="w-5 h-5" />
                <span>Run Simulation</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Impact Preview */}
      <div className="card bg-gray-50">
        <h3 className="font-semibold text-gray-900 mb-4">Expected Impact Changes</h3>
        <div className="grid md:grid-cols-4 gap-4">
          <div className="text-center p-4 bg-white rounded-lg">
            <div className="text-sm text-gray-600 mb-1">GDP Impact</div>
            <div className="text-lg font-semibold text-blue-600">
              {((adjustments.budget_increase || 0) * 5 + (adjustments.tax_rate || 0) * -3).toFixed(1)}%
            </div>
          </div>
          <div className="text-center p-4 bg-white rounded-lg">
            <div className="text-sm text-gray-600 mb-1">Public Support</div>
            <div className="text-lg font-semibold text-green-600">
              {((adjustments.subsidy_increase || 0) * 10 - Math.abs(adjustments.tax_rate || 0) * 15).toFixed(1)}%
            </div>
          </div>
          <div className="text-center p-4 bg-white rounded-lg">
            <div className="text-sm text-gray-600 mb-1">Implementation Time</div>
            <div className="text-lg font-semibold text-orange-600">
              {adjustments.implementation_speed ? 
                (adjustments.implementation_speed > 0 ? 'Faster' : 'Slower') : 
                'Same'
              }
            </div>
          </div>
          <div className="text-center p-4 bg-white rounded-lg">
            <div className="text-sm text-gray-600 mb-1">Risk Level</div>
            <div className="text-lg font-semibold text-red-600">
              {Math.abs(adjustments.tax_rate || 0) > 0.2 ? 'Higher' : 'Normal'}
            </div>
          </div>
        </div>
      </div>

      {/* Scenario Presets */}
      <div className="card">
        <h3 className="font-semibold text-gray-900 mb-4">Quick Scenarios</h3>
        <div className="grid md:grid-cols-3 gap-4">
          <button
            onClick={() => {
              setAdjustments({ subsidy_increase: 0.5, budget_increase: 0.3, tax_rate: 0.1, implementation_speed: 0 })
            }}
            className="p-4 border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 text-left transition-colors"
          >
            <h4 className="font-medium text-gray-900 mb-1">Growth Focus</h4>
            <p className="text-sm text-gray-600">Increase subsidies and budget for maximum impact</p>
          </button>
          
          <button
            onClick={() => {
              setAdjustments({ subsidy_increase: 0.2, budget_increase: 0, tax_rate: 0.2, implementation_speed: 0.2 })
            }}
            className="p-4 border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 text-left transition-colors"
          >
            <h4 className="font-medium text-gray-900 mb-1">Balanced Approach</h4>
            <p className="text-sm text-gray-600">Moderate increases with faster implementation</p>
          </button>
          
          <button
            onClick={() => {
              setAdjustments({ subsidy_increase: -0.2, budget_increase: -0.3, tax_rate: -0.1, implementation_speed: 0 })
            }}
            className="p-4 border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 text-left transition-colors"
          >
            <h4 className="font-medium text-gray-900 mb-1">Fiscal Conservative</h4>
            <p className="text-sm text-gray-600">Reduce spending and lower tax burden</p>
          </button>
        </div>
      </div>
    </div>
  )
}
