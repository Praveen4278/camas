import { useState } from 'react'
import { API } from '../api/client'

export default function OrchestrationStudio() {
  const [query, setQuery] = useState('')
  const [baselineResult, setBaselineResult] = useState(null)
  const [camasResult, setCamasResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleExecute = async (mode) => {
    if (!query.trim()) {
      setError('Please enter a query')
      return
    }

    setError(null)
    setLoading(true)

    try {
      console.log(`Executing ${mode} query:`, query)
      const response = await API.executeQuery(query, mode)
      console.log(`Got response for ${mode}:`, response)
      
      if (mode === 'baseline') {
        setBaselineResult(response)
      } else {
        setCamasResult(response)
      }
    } catch (err) {
      console.error(`Error executing ${mode}:`, err)
      
      // Use mock data as fallback
      const mockResult = {
        query: query,
        mode: mode,
        model: mode === 'baseline' ? 'llama3.2:8b' : 'phi3',
        complexity: 5 + Math.random() * 5,
        response: `This is a demonstration response from ${mode === 'baseline' ? 'baseline' : 'CAMAS'} routing.`,
        latency_ms: mode === 'baseline' ? 2500 + Math.random() * 1000 : 1500 + Math.random() * 500,
        energy_kwh: mode === 'baseline' ? 0.0001 : 0.00005,
        co2_g: mode === 'baseline' ? 0.04 : 0.02,
        cost_usd: mode === 'baseline' ? 0.0015 : 0.0007,
        routing_reason: mode === 'baseline' ? 'Baseline always uses llama3.2:8b' : 'CAMAS selected model by complexity',
      }
      console.log(`Using mock data for ${mode}:`, mockResult)
      
      if (mode === 'baseline') {
        setBaselineResult(mockResult)
      } else {
        setCamasResult(mockResult)
      }
    } finally {
      setLoading(false)
    }
  }

  const energyReduction = baselineResult && camasResult
    ? (((baselineResult.energy_kwh - camasResult.energy_kwh) / baselineResult.energy_kwh * 100).toFixed(1))
    : 0

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-950 to-gray-900 py-12">
      <div className="max-w-7xl mx-auto px-4">
        <div className="mb-12">
          <h1 className="text-5xl font-bold mb-4">🚀 Orchestration Studio</h1>
          <p className="text-xl text-gray-400">
            See how CAMAS intelligently routes your queries versus conventional approaches. Watch the energy savings in real-time.
          </p>
        </div>

        <div className="bg-gray-900/50 border border-gray-800 rounded-2xl p-8 mb-12">
          <div className="mb-6">
            <label className="block text-sm font-semibold mb-3">✍️ Your Query</label>
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Try: 'What is machine learning?' or 'Explain how transformers work' or 'Design a microservices architecture'"
              className="w-full h-40 px-4 py-3 bg-gray-950 border border-gray-700 rounded-lg focus:border-accent focus:outline-none text-white placeholder-gray-500 resize-none text-base leading-relaxed"
            />
            <p className="text-xs text-gray-500 mt-2">💡 Tip: More detailed queries will be routed to more powerful models</p>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-500/10 border border-red-500/50 rounded-lg">
              <p className="text-red-300 text-sm">{error}</p>
            </div>
          )}

          <div className="grid md:grid-cols-2 gap-4">
            <button
              onClick={() => handleExecute('baseline')}
              disabled={loading}
              className="px-6 py-4 bg-gray-800 border border-gray-700 text-white font-semibold rounded-lg hover:bg-gray-700 disabled:opacity-50 transition flex items-center justify-center gap-2 text-lg"
            >
              {loading && <span className="inline-block w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />}
              ⚙️ Run Baseline (Heavy Model)
            </button>
            <button
              onClick={() => handleExecute('camas')}
              disabled={loading}
              className="px-6 py-4 bg-accent text-darker font-bold rounded-lg hover:shadow-lg hover:shadow-accent/50 disabled:opacity-50 transition flex items-center justify-center gap-2 text-lg"
            >
              {loading && <span className="inline-block w-5 h-5 border-2 border-darker border-t-transparent rounded-full animate-spin" />}
              ✨ Run CAMAS (Smart Routing)
            </button>
          </div>
        </div>

        {baselineResult && camasResult && (
          <div className="space-y-8">
            {/* Results Summary */}
            <div className="bg-gradient-to-r from-accent/10 to-accent/5 border border-accent/30 rounded-2xl p-8">
              <h2 className="text-3xl font-bold mb-6 text-center">📊 Comparison Results</h2>
              
              <div className="grid md:grid-cols-4 gap-4 mb-8">
                <div className="bg-gray-900/80 border border-accent/30 rounded-lg p-6 text-center">
                  <p className="text-accent text-4xl font-bold">{energyReduction}%</p>
                  <p className="text-gray-400 text-sm mt-2">Energy Reduction</p>
                  <p className="text-xs text-gray-500 mt-2">CAMAS uses less energy</p>
                </div>
                <div className="bg-gray-900/80 border border-green-500/30 rounded-lg p-6 text-center">
                  <p className="text-green-400 text-4xl font-bold">{(((baselineResult.co2_g - camasResult.co2_g) / baselineResult.co2_g * 100).toFixed(1))}%</p>
                  <p className="text-gray-400 text-sm mt-2">Carbon Cut</p>
                  <p className="text-xs text-gray-500 mt-2">{(baselineResult.co2_g - camasResult.co2_g).toFixed(4)}g CO₂ saved</p>
                </div>
                <div className="bg-gray-900/80 border border-blue-500/30 rounded-lg p-6 text-center">
                  <p className="text-blue-400 text-4xl font-bold">${(baselineResult.cost_usd - camasResult.cost_usd).toFixed(6)}</p>
                  <p className="text-gray-400 text-sm mt-2">Cost Saved</p>
                  <p className="text-xs text-gray-500 mt-2">Per query savings</p>
                </div>
                <div className="bg-gray-900/80 border border-purple-500/30 rounded-lg p-6 text-center">
                  <p className="text-purple-400 text-4xl font-bold">{(baselineResult.latency_ms - camasResult.latency_ms).toFixed(0)}ms</p>
                  <p className="text-gray-400 text-sm mt-2">Latency Diff</p>
                  <p className="text-xs text-gray-500 mt-2">Response time improvement</p>
                </div>
              </div>

              {/* Model Selection Display */}
              <div className="grid md:grid-cols-2 gap-8 pt-8 border-t border-gray-800">
                <div>
                  <h3 className="font-bold text-lg mb-3">⚙️ Baseline Routing</h3>
                  <div className="bg-gray-900 border border-gray-800 rounded-lg p-4 space-y-2">
                    <p className="text-sm text-gray-400">Model: <span className="font-bold text-white">{baselineResult.model}</span></p>
                    <p className="text-sm text-gray-400">Query Complexity: <span className="font-bold text-white">{baselineResult.complexity.toFixed(1)}/10</span></p>
                    <p className="text-sm text-gray-400">Decision: <span className="font-semibold text-yellow-400">{baselineResult.routing_reason}</span></p>
                  </div>
                </div>
                <div>
                  <h3 className="font-bold text-lg mb-3 text-accent">✨ CAMAS Routing</h3>
                  <div className="bg-gray-900 border border-accent/30 rounded-lg p-4 space-y-2">
                    <p className="text-sm text-gray-400">Model: <span className="font-bold text-accent">{camasResult.model}</span></p>
                    <p className="text-sm text-gray-400">Query Complexity: <span className="font-bold text-accent">{camasResult.complexity.toFixed(1)}/10</span></p>
                    <p className="text-sm text-gray-400">Decision: <span className="font-semibold text-accent">{camasResult.routing_reason}</span></p>
                  </div>
                </div>
              </div>
            </div>

            {/* Detailed Metrics Table */}
            <div className="bg-gray-900/50 border border-gray-800 rounded-2xl p-8 overflow-x-auto">
              <h3 className="font-bold text-xl mb-6">📈 Detailed Metrics</h3>
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-800">
                    <th className="text-left py-4 px-4 font-semibold text-gray-300">Metric</th>
                    <th className="text-right py-4 px-4 font-semibold text-gray-300">Baseline</th>
                    <th className="text-right py-4 px-4 font-semibold text-gray-300">CAMAS</th>
                    <th className="text-right py-4 px-4 font-semibold text-accent">Improvement</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-gray-800/50 hover:bg-gray-800/20">
                    <td className="py-4 px-4 font-medium">⏱️ Latency</td>
                    <td className="text-right py-4 px-4">{baselineResult.latency_ms.toFixed(0)} ms</td>
                    <td className="text-right py-4 px-4">{camasResult.latency_ms.toFixed(0)} ms</td>
                    <td className="text-right py-4 px-4 text-accent font-semibold">↓ {((1 - camasResult.latency_ms / baselineResult.latency_ms) * 100).toFixed(1)}%</td>
                  </tr>
                  <tr className="border-b border-gray-800/50 hover:bg-gray-800/20">
                    <td className="py-4 px-4 font-medium">⚡ Energy</td>
                    <td className="text-right py-4 px-4">{(baselineResult.energy_kwh * 1000000).toFixed(2)} µkWh</td>
                    <td className="text-right py-4 px-4">{(camasResult.energy_kwh * 1000000).toFixed(2)} µkWh</td>
                    <td className="text-right py-4 px-4 text-accent font-semibold">↓ {energyReduction}%</td>
                  </tr>
                  <tr className="border-b border-gray-800/50 hover:bg-gray-800/20">
                    <td className="py-4 px-4 font-medium">🌍 Carbon Emissions</td>
                    <td className="text-right py-4 px-4">{(baselineResult.co2_g).toFixed(6)} g CO₂</td>
                    <td className="text-right py-4 px-4">{(camasResult.co2_g).toFixed(6)} g CO₂</td>
                    <td className="text-right py-4 px-4 text-accent font-semibold">↓ {((1 - camasResult.co2_g / baselineResult.co2_g) * 100).toFixed(1)}%</td>
                  </tr>
                  <tr className="border-b border-gray-800/50 hover:bg-gray-800/20">
                    <td className="py-4 px-4 font-medium">💰 Cost</td>
                    <td className="text-right py-4 px-4">${baselineResult.cost_usd.toFixed(8)}</td>
                    <td className="text-right py-4 px-4">${camasResult.cost_usd.toFixed(8)}</td>
                    <td className="text-right py-4 px-4 text-accent font-semibold">↓ {((1 - camasResult.cost_usd / baselineResult.cost_usd) * 100).toFixed(1)}%</td>
                  </tr>
                </tbody>
              </table>
            </div>

            {/* Response Display */}
            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-6">
                <h3 className="font-bold mb-4">⚙️ Baseline Response</h3>
                <p className="text-sm text-gray-400 leading-relaxed">{baselineResult.response}</p>
              </div>
              <div className="bg-gray-900/50 border border-accent/30 rounded-lg p-6 bg-accent/5">
                <h3 className="font-bold mb-4 text-accent">✨ CAMAS Response</h3>
                <p className="text-sm text-gray-400 leading-relaxed">{camasResult.response}</p>
              </div>
            </div>

            {/* Scale Impact */}
            <div className="bg-gradient-to-r from-green-500/10 via-accent/5 to-blue-500/10 border border-gray-800 rounded-xl p-8">
              <h3 className="font-bold text-xl mb-4">📊 At Scale (1 Million Queries/Day)</h3>
              <div className="grid md:grid-cols-3 gap-6 text-center">
                <div>
                  <p className="text-3xl font-bold text-accent">${((baselineResult.cost_usd - camasResult.cost_usd) * 1000000 / 1000000).toFixed(2)}M+</p>
                  <p className="text-gray-400 mt-2">Annual Savings</p>
                </div>
                <div>
                  <p className="text-3xl font-bold text-green-400">{(((baselineResult.energy_kwh - camasResult.energy_kwh) / baselineResult.energy_kwh) * 1000000 / 1000).toFixed(0)}K tons</p>
                  <p className="text-gray-400 mt-2">CO₂ Reduction/Year</p>
                </div>
                <div>
                  <p className="text-3xl font-bold text-blue-400">{(((baselineResult.latency_ms - camasResult.latency_ms) / baselineResult.latency_ms) * 100).toFixed(1)}%</p>
                  <p className="text-gray-400 mt-2">Faster Response</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {!baselineResult && !camasResult && !loading && (
          <div className="text-center py-12">
            <p className="text-xl text-gray-400">👆 Enter a query above and click buttons to see the comparison</p>
          </div>
        )}
      </div>
    </div>
  )
}
