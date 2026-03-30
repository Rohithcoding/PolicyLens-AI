import { Brain } from 'lucide-react'

export function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-16">
      <div className="relative">
        <div className="w-16 h-16 border-4 border-primary-200 rounded-full animate-pulse" />
        <div className="absolute top-0 left-0 w-16 h-16 border-4 border-primary-600 border-t-transparent rounded-full animate-spin" />
        <div className="absolute inset-2 flex items-center justify-center">
          <Brain className="w-6 h-6 text-primary-600 animate-pulse" />
        </div>
      </div>
      
      <div className="mt-6 text-center">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Agents Working</h3>
        <div className="space-y-2 text-sm text-gray-600">
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-success-500 rounded-full animate-pulse" />
            <span>Policy Understanding Agent analyzing text...</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse delay-75" />
            <span>Simulation Agent creating population model...</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-warning-500 rounded-full animate-pulse delay-150" />
            <span>Impact Prediction Agent calculating outcomes...</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse delay-300" />
            <span>Sentiment Agent analyzing public opinion...</span>
          </div>
        </div>
      </div>
      
      <div className="mt-6">
        <div className="w-64 h-2 bg-gray-200 rounded-full overflow-hidden">
          <div className="h-full bg-gradient-to-r from-primary-500 to-primary-600 rounded-full animate-pulse" 
               style={{ width: '75%', animation: 'shimmer 2s infinite' }} />
        </div>
        <p className="text-xs text-gray-500 mt-2 text-center">This usually takes 15-30 seconds</p>
      </div>
    </div>
  )
}
