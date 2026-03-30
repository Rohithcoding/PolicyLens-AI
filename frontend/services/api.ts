import axios from 'axios'
import { PolicyInput, SimulationResult } from '@/types/policy'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds timeout
})

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log('Making request:', config.method?.toUpperCase(), config.url)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export const analyzePolicy = async (policyInput: PolicyInput): Promise<SimulationResult> => {
  try {
    const response = await api.post('/api/policy/analyze', policyInput)
    return response.data
  } catch (error) {
    console.error('Policy analysis error:', error)
    throw new Error('Failed to analyze policy')
  }
}

export const runWhatIfSimulation = async (
  policyText: string,
  adjustments: Record<string, number>
): Promise<SimulationResult> => {
  try {
    const response = await api.post('/api/policy/what-if', {
      policy_text: policyText,
      adjustments
    })
    return response.data
  } catch (error) {
    console.error('What-if simulation error:', error)
    throw new Error('Failed to run what-if simulation')
  }
}

export const getPolicySectors = async () => {
  try {
    const response = await api.get('/api/policy/sectors')
    return response.data
  } catch (error) {
    console.error('Get sectors error:', error)
    throw new Error('Failed to get policy sectors')
  }
}

export const getDefaultPopulation = async () => {
  try {
    const response = await api.get('/api/simulation/population/default')
    return response.data
  } catch (error) {
    console.error('Get population error:', error)
    throw new Error('Failed to get default population')
  }
}

export const getDemographicOptions = async () => {
  try {
    const response = await api.get('/api/simulation/demographics')
    return response.data
  } catch (error) {
    console.error('Get demographics error:', error)
    throw new Error('Failed to get demographic options')
  }
}

export const healthCheck = async () => {
  try {
    const response = await api.get('/health')
    return response.data
  } catch (error) {
    console.error('Health check error:', error)
    throw new Error('API is not available')
  }
}
