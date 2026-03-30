'use client'

import { useState } from 'react'
import { PolicyInput } from '@/components/PolicyInput'
import { SimulationResults } from '@/components/SimulationResults'
import { WhatIfSimulation } from '@/components/WhatIfSimulation'
import { Header } from '@/components/Header'
import { Footer } from '@/components/Footer'
import { LoadingSpinner } from '@/components/LoadingSpinner'
import { SimulationResult } from '@/types/policy'
import { analyzePolicy } from '@/services/api'
import toast from 'react-hot-toast'

export default function Home() {
  const [currentResult, setCurrentResult] = useState<SimulationResult | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [activeTab, setActiveTab] = useState<'input' | 'results' | 'whatif'>('input')

  const handlePolicyAnalysis = async (policyText: string, policyTitle?: string) => {
    setIsAnalyzing(true)
    setActiveTab('results')
    
    try {
      const result = await analyzePolicy({ text: policyText, title: policyTitle })
      setCurrentResult(result)
      toast.success('Policy analysis completed successfully!')
    } catch (error) {
      console.error('Analysis error:', error)
      toast.error('Failed to analyze policy. Please try again.')
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleWhatIfAnalysis = async (adjustments: Record<string, number>) => {
    if (!currentResult) {
      toast.error('Please analyze a policy first')
      return
    }

    setIsAnalyzing(true)
    
    try {
      // Reconstruct the original policy text from the current result
      const policyText = currentResult.policy_analysis.key_changes.join('. ')
      
      const result = await analyzePolicy({
        text: policyText,
        adjustments
      })
      
      setCurrentResult(result)
      toast.success('What-if simulation completed!')
    } catch (error) {
      console.error('What-if error:', error)
      toast.error('Failed to run what-if simulation. Please try again.')
    } finally {
      setIsAnalyzing(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <main className="flex-1 container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-6xl font-bold text-gradient mb-4">
              PolicyLens AI
            </h1>
            <p className="text-xl text-gray-600 mb-2">
              Test Before You Implement
            </p>
            <p className="text-lg text-gray-500 max-w-2xl mx-auto">
              Simulate policies before they impact millions. AI-powered analysis for better decision-making.
            </p>
          </div>

          {/* Tab Navigation */}
          <div className="flex justify-center mb-8">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-1 inline-flex">
              <button
                onClick={() => setActiveTab('input')}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  activeTab === 'input'
                    ? 'bg-primary-600 text-white'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                1. Policy Input
              </button>
              <button
                onClick={() => setActiveTab('results')}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  activeTab === 'results'
                    ? 'bg-primary-600 text-white'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
                disabled={!currentResult}
              >
                2. Results
              </button>
              <button
                onClick={() => setActiveTab('whatif')}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  activeTab === 'whatif'
                    ? 'bg-primary-600 text-white'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
                disabled={!currentResult}
              >
                3. What-If
              </button>
            </div>
          </div>

          {/* Content Area */}
          <div className="animate-fade-in">
            {isAnalyzing ? (
              <LoadingSpinner />
            ) : (
              <>
                {activeTab === 'input' && (
                  <PolicyInput onAnalyze={handlePolicyAnalysis} />
                )}
                
                {activeTab === 'results' && currentResult && (
                  <SimulationResults result={currentResult} />
                )}
                
                {activeTab === 'whatif' && currentResult && (
                  <WhatIfSimulation 
                    currentResult={currentResult}
                    onSimulate={handleWhatIfAnalysis}
                  />
                )}
              </>
            )}
          </div>

          {/* Features Section */}
          {activeTab === 'input' && (
            <div className="mt-16 grid md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold mb-2">Policy Analysis</h3>
                <p className="text-gray-600">AI-powered understanding of policy content and stakeholder impact</p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-success-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-success-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold mb-2">Impact Simulation</h3>
                <p className="text-gray-600">Synthetic population modeling to predict economic and social outcomes</p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-warning-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-warning-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold mb-2">Real-time Results</h3>
                <p className="text-gray-600">Instant insights with confidence scores and actionable recommendations</p>
              </div>
            </div>
          )}
        </div>
      </main>

      <Footer />
    </div>
  )
}
