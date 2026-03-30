'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { Send, FileText, Zap } from 'lucide-react'

interface PolicyInputProps {
  onAnalyze: (policyText: string, policyTitle?: string) => void
}

interface FormData {
  policyText: string
  policyTitle: string
}

export function PolicyInput({ onAnalyze }: PolicyInputProps) {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const { register, handleSubmit, formState: { errors }, watch } = useForm<FormData>()

  const watchedText = watch('policyText')

  const onSubmit = async (data: FormData) => {
    setIsSubmitting(true)
    try {
      await onAnalyze(data.policyText, data.policyTitle)
    } finally {
      setIsSubmitting(false)
    }
  }

  const samplePolicies = [
    {
      title: "Agricultural Reform",
      text: "The government proposes to increase agricultural subsidies by 20% and provide low-interest loans to farmers for purchasing modern equipment. This policy aims to boost agricultural productivity and reduce rural poverty."
    },
    {
      title: "Digital Education Initiative",
      text: "Implementation of a nationwide digital education platform providing free online courses and digital literacy programs. The initiative includes distribution of tablets to underserved communities and teacher training programs."
    },
    {
      title: "Green Energy Transition",
      text: "A comprehensive policy to transition 50% of energy production to renewable sources by 2030. Includes tax incentives for solar panel installation, wind farm development, and electric vehicle adoption."
    }
  ]

  const loadSamplePolicy = (index: number) => {
    const sample = samplePolicies[index]
    // This would typically use the form's setValue method
    const event = new CustomEvent('loadSample', { detail: sample })
    window.dispatchEvent(event)
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="card">
        <div className="flex items-center space-x-3 mb-6">
          <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
            <FileText className="w-6 h-6 text-primary-600" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Policy Input</h2>
            <p className="text-gray-600">Enter your policy text for AI analysis</p>
          </div>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Policy Title */}
          <div>
            <label htmlFor="policyTitle" className="block text-sm font-medium text-gray-700 mb-2">
              Policy Title (Optional)
            </label>
            <input
              id="policyTitle"
              type="text"
              placeholder="e.g., Agricultural Reform Bill 2024"
              className="input"
              {...register('policyTitle')}
            />
          </div>

          {/* Policy Text */}
          <div>
            <label htmlFor="policyText" className="block text-sm font-medium text-gray-700 mb-2">
              Policy Text *
            </label>
            <textarea
              id="policyText"
              placeholder="Enter the complete policy text here. The AI will analyze its content, identify stakeholders, and predict impacts..."
              className="textarea"
              rows={8}
              {...register('policyText', { 
                required: 'Policy text is required',
                minLength: {
                  value: 50,
                  message: 'Policy text must be at least 50 characters long'
                }
              })}
            />
            {errors.policyText && (
              <p className="text-danger-600 text-sm mt-1">{errors.policyText.message}</p>
            )}
            
            {/* Character count */}
            <div className="text-right mt-2">
              <span className={`text-sm ${watchedText?.length > 50 ? 'text-success-600' : 'text-gray-500'}`}>
                {watchedText?.length || 0} / 5000 characters
              </span>
            </div>
          </div>

          {/* Sample Policies */}
          <div>
            <p className="text-sm font-medium text-gray-700 mb-3">Try a sample policy:</p>
            <div className="grid md:grid-cols-3 gap-3">
              {samplePolicies.map((sample, index) => (
                <button
                  key={index}
                  type="button"
                  onClick={() => loadSamplePolicy(index)}
                  className="text-left p-3 border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors"
                >
                  <h4 className="font-medium text-gray-900 text-sm mb-1">{sample.title}</h4>
                  <p className="text-xs text-gray-600 line-clamp-2">{sample.text}</p>
                </button>
              ))}
            </div>
          </div>

          {/* Submit Button */}
          <div className="flex justify-center">
            <button
              type="submit"
              disabled={isSubmitting || !watchedText || watchedText.length < 50}
              className="btn-primary px-8 py-3 flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <Zap className="w-5 h-5" />
                  <span>Analyze Policy</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Info Section */}
      <div className="mt-8 grid md:grid-cols-3 gap-6">
        <div className="text-center p-4">
          <div className="w-12 h-12 bg-success-100 rounded-full flex items-center justify-center mx-auto mb-3">
            <Zap className="w-6 h-6 text-success-600" />
          </div>
          <h3 className="font-semibold mb-2">Fast Analysis</h3>
          <p className="text-sm text-gray-600">Get comprehensive policy insights in seconds</p>
        </div>
        
        <div className="text-center p-4">
          <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-3">
            <Send className="w-6 h-6 text-primary-600" />
          </div>
          <h3 className="font-semibold mb-2">Multi-Agent AI</h3>
          <p className="text-sm text-gray-600">Four specialized AI agents analyze different aspects</p>
        </div>
        
        <div className="text-center p-4">
          <div className="w-12 h-12 bg-warning-100 rounded-full flex items-center justify-center mx-auto mb-3">
            <FileText className="w-6 h-6 text-warning-600" />
          </div>
          <h3 className="font-semibold mb-2">Actionable Insights</h3>
          <p className="text-sm text-gray-600">Get recommendations and risk assessments</p>
        </div>
      </div>
    </div>
  )
}
