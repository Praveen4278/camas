import axios from 'axios'

// For local development, connect to backend at localhost:8000
// For Vercel deployment, use mock data
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'mock://' 
  : (import.meta.env.VITE_API_URL || 'http://localhost:8000')

const client = axios.create({
  baseURL: API_BASE_URL === 'mock://' ? 'http://localhost:8000' : API_BASE_URL,
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Mock data generator using only your 3 models from research paper
function generateMockResult(query, mode) {
  const queryLower = query.toLowerCase()
  
  // Complexity scoring
  let complexity = Math.min(10.0, (query.split(' ').length / 3) + (query.length / 100))
  
  // Boost complexity for complex queries
  if (queryLower.includes('design') || queryLower.includes('architecture') || 
      queryLower.includes('complex') || queryLower.includes('explain deep') ||
      queryLower.includes('abstract')) {
    complexity = Math.min(10, complexity + 3)
  }
  
  // Model selection - only 3 models from research paper
  let model, energy, co2
  if (mode === 'baseline') {
    // Baseline always uses llama3.2:8b
    model = 'llama3.2:8b'
    energy = 0.000111
    co2 = 0.0446
  } else {
    // CAMAS intelligent routing
    if (complexity < 4) {
      model = 'phi3'
      energy = 0.000018
      co2 = 0.0072
    } else if (complexity < 8) {
      model = 'llama3.2:3b'
      energy = 0.000047
      co2 = 0.0188
    } else {
      model = 'llama3.2:8b'
      energy = 0.000087
      co2 = 0.0349
    }
  }
  
  return {
    query: query,
    mode: mode,
    model: model,
    complexity: complexity,
    response: `This is an intelligent response demonstrating CAMAS' ${mode === 'baseline' ? 'baseline' : 'smart routing'} approach.`,
    latency_ms: 1500 + (complexity * 150) + (Math.random() * 500),
    energy_kwh: energy,
    co2_g: co2,
    cost_usd: energy * 0.15, // Rough estimate: $0.15 per kWh
    routing_reason: mode === 'baseline' 
      ? 'Baseline always uses llama3.2:8b regardless of complexity'
      : `CAMAS routed to ${model} (Complexity: ${complexity.toFixed(1)}/10)`,
  }
}

// Response interceptor for local API
client.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    // If local API fails, return mock data as fallback
    if (!process.env.NODE_ENV === 'production') {
      console.log('Using mock data fallback')
    }
    return Promise.reject(error)
  }
)

export default client

export const API = {
  // Single query execution
  executeQuery: async (query, mode = 'camas') => {
    try {
      // Try to call backend API first (for local development)
      if (process.env.NODE_ENV !== 'production') {
        const response = await client.post('/query', { query, mode })
        return response
      }
    } catch (error) {
      console.log('Backend unavailable, using mock data')
    }
    
    // Use mock data (for Vercel or if backend fails)
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(generateMockResult(query, mode))
      }, 800) // Simulate 800ms response time
    })
  },

  // Health check
  health: async () => {
    try {
      return await client.get('/health')
    } catch {
      return { status: 'mock' }
    }
  },

  // Placeholder methods for compatibility
  startExperiment: (mode, maxQueries = null) =>
    Promise.reject(new Error('Not available in demo')),

  getExperimentSummary: (runId) =>
    Promise.reject(new Error('Not available in demo')),

  listExperiments: () =>
    Promise.reject(new Error('Not available in demo')),

  getRoutingDistribution: (runId) =>
    Promise.reject(new Error('Not available in demo')),

  generateReports: () =>
    Promise.reject(new Error('Not available in demo')),

  getConfig: () =>
    Promise.reject(new Error('Not available in demo')),
}
