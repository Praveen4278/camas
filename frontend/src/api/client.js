import axios from 'axios'

// For Vercel deployment, use mock data
// For local development, connect to backend at localhost:8000
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'mock://' 
  : (import.meta.env.VITE_API_URL || 'http://localhost:8000')

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
client.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor with mock data fallback
client.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('API Error:', error)
    
    // Mock data for production (Vercel)
    if (process.env.NODE_ENV === 'production' || API_BASE_URL === 'mock://') {
      console.log('Using mock data')
      // Request will be intercepted before sending
    }
    
    return Promise.reject(error)
  }
)

// Mock data interceptor for production
if (API_BASE_URL === 'mock://') {
  client.interceptors.request.use((config) => {
    // Intercept POST /query and return mock data
    if (config.url?.includes('/query') || config.url === '/query') {
      const body = config.data
      const query = body?.query || ''
      const mode = body?.mode || 'camas'
      
      // Simulate API delay
      return new Promise(resolve => {
        setTimeout(() => {
          const complexity = Math.min(10.0, 2.0 + query.length / 20.0)
          const isComplex = query.toLowerCase().includes('complex') || query.toLowerCase().includes('deep') || query.toLowerCase().includes('explain')
          
          const result = {
            query: query,
            mode: mode,
            model: mode === 'baseline' ? 'samantha-mistral' : (complexity > 5 ? 'samantha-mistral' : 'llama3.2'),
            complexity: complexity + (isComplex ? 3 : 0),
            response: `Response to: ${query}`,
            latency_ms: mode === 'baseline' ? 3000 + Math.random() * 1000 : 1500 + Math.random() * 1000,
            energy_kwh: mode === 'baseline' ? 0.00008 + Math.random() * 0.00002 : 0.00002 + Math.random() * 0.00005,
            co2_g: mode === 'baseline' ? 0.04 : 0.01,
            cost_usd: mode === 'baseline' ? 0.0014 : 0.0002,
            routing_reason: mode === 'baseline' ? 'Baseline always uses heavy model' : 'CAMAS routed based on complexity',
          }
          
          resolve({
            ...config,
            adapter: async () => ({ status: 200, data: result })
          })
        }, 500)
      })
    }
    
    // Health check
    if (config.url?.includes('/health') || config.url === '/health') {
      return {
        ...config,
        adapter: async () => ({ status: 200, data: { status: 'ok' } })
      }
    }
    
    return config
  })
}

export default client

export const API = {
  // Health check
  health: () => client.get('/health'),

  // Single query execution
  executeQuery: (query, mode = 'camas') =>
    client.post('/query', { query, mode }),

  // Experiment management (won't work on Vercel, placeholder)
  startExperiment: (mode, maxQueries = null) =>
    Promise.reject(new Error('Not available on serverless')),

  getExperimentSummary: (runId) =>
    Promise.reject(new Error('Not available on serverless')),

  listExperiments: () =>
    Promise.reject(new Error('Not available on serverless')),

  getRoutingDistribution: (runId) =>
    Promise.reject(new Error('Not available on serverless')),

  // Reports
  generateReports: () =>
    Promise.reject(new Error('Not available on serverless')),

  // Config
  getConfig: () =>
    Promise.reject(new Error('Not available on serverless')),
}
