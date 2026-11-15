import { useState } from 'react'
import { API } from '../api/client'

export default function OrchestrationStudio() {
  const [query, setQuery] = useState('')
  const [baselineResult, setBaselineResult] = useState(null)
  const [camasResult, setCamasResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleExecute = async () => {
    if (!query.trim()) {
      setError('Please enter a query')
      return
    }

    setError(null)
    setLoading(true)
    
    try {
      // Run both queries in parallel
      console.log('Executing both baseline and CAMAS queries for:', query)
      const [baselineResp, camasResp] = await Promise.all([
        API.executeQuery(query, 'baseline'),
        API.executeQuery(query, 'camas')
      ])
      
      console.log('Got both responses:', { baseline: baselineResp, camas: camasResp })
      console.log('Energy savings: Baseline uses', baselineResp.model, '-> CAMAS uses', camasResp.model)
      console.log('Energy reduction:', camasResp.energy_savings_percent, '%')
      console.log('BEFORE setState - camasResult would become:', camasResp)
      setBaselineResult(baselineResp)
      setCamasResult(camasResp)
      console.log('AFTER setState called with:', { baseline: baselineResp.energy_savings_percent, camas: camasResp.energy_savings_percent })
    } catch (err) {
      console.error('Error executing queries:', err)
      setError(`Error: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const energyReduction = camasResult?.energy_savings_percent || 0

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-950 to-gray-900 py-12">
      <div className="max-w-7xl mx-auto px-4">
        <div className="mb-12">
          <h1 className="text-5xl font-bold mb-4">🚀 Orchestration Studio</h1>
          <p className="text-xl text-gray-400">
            Enter different queries to see how CAMAS intelligently routes to different models based on complexity. The more complex your query, the more energy savings you'll see.
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
            <p className="text-xs text-gray-500 mt-2">💡 Tip: Try different queries from simple ("What is AI?") to complex ("Design a distributed ML system") to see different model selections and energy savings</p>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-500/10 border border-red-500/50 rounded-lg">
              <p className="text-red-300 text-sm">{error}</p>
            </div>
          )}

          <div className="space-y-3">
            <button
              onClick={() => handleExecute()}
              disabled={loading}
              className="w-full px-6 py-4 bg-accent text-darker font-bold rounded-lg hover:shadow-lg hover:shadow-accent/50 disabled:opacity-50 transition flex items-center justify-center gap-2 text-lg"
            >
              {loading && <span className="inline-block w-5 h-5 border-2 border-darker border-t-transparent rounded-full animate-spin" />}
              ⚡ Analyze Query & Compare
            </button>
            <p className="text-xs text-gray-500 text-center">Runs baseline (llama3.2:8b) vs CAMAS smart routing for comparison</p>
          </div>
        </div>

        {(baselineResult || camasResult) && (
          <div className="space-y-8">
            {/* Comparison Results - Show when both exist */}
            {baselineResult && camasResult && (
              <div className="bg-gradient-to-r from-accent/10 to-accent/5 border border-accent/30 rounded-2xl p-8">
                <h2 className="text-3xl font-bold mb-6 text-center">📊 Comparison Results</h2>
                <p className="text-xs text-gray-400 text-center mb-4">Query: "{query}"</p>
                
                <div className="grid md:grid-cols-4 gap-4 mb-8">
                  <div className="bg-gray-900/80 border border-accent/30 rounded-lg p-6 text-center">
                    <p className="text-accent text-4xl font-bold">{camasResult.energy_savings_percent}%</p>
                    <p className="text-gray-400 text-sm mt-2">Energy Reduction</p>
                  </div>
                  <div className="bg-gray-900/80 border border-green-500/30 rounded-lg p-6 text-center">
                    <p className="text-green-400 text-4xl font-bold">{camasResult.co2_savings_percent}%</p>
                    <p className="text-gray-400 text-sm mt-2">Carbon Cut</p>
                    <p className="text-xs text-gray-500 mt-2">{(baselineResult.co2_g - camasResult.co2_g).toFixed(4)}g saved</p>
                  </div>
                  <div className="bg-gray-900/80 border border-blue-500/30 rounded-lg p-6 text-center">
                    <p className="text-blue-400 text-4xl font-bold">${camasResult.cost_savings_usd.toFixed(6)}</p>
                    <p className="text-gray-400 text-sm mt-2">Cost Saved</p>
                  </div>
                  <div className="bg-gray-900/80 border border-purple-500/30 rounded-lg p-6 text-center">
                    <p className="text-purple-400 text-4xl font-bold">{camasResult.latency_savings_ms}ms</p>
                    <p className="text-gray-400 text-sm mt-2">Latency Improvement</p>
                  </div>
                </div>

                {/* Model Comparison */}
                <div className="grid md:grid-cols-2 gap-8 pt-8 border-t border-gray-800">
                  <div>
                    <h3 className="font-bold text-lg mb-3">⚙️ Baseline</h3>
                    <div className="bg-gray-900 border border-gray-800 rounded-lg p-4 space-y-2">
                      <p className="text-sm"><span className="text-gray-400">Model:</span> <span className="font-bold text-white">{baselineResult.model}</span></p>
                      <p className="text-sm"><span className="text-gray-400">Complexity:</span> <span className="font-bold">{baselineResult.complexity.toFixed(1)}/10</span></p>
                      <p className="text-sm"><span className="text-gray-400">Energy:</span> <span className="font-bold text-yellow-400">{(baselineResult.energy_kwh * 1000000).toFixed(2)} µkWh</span></p>
                      <p className="text-sm"><span className="text-gray-400">CO₂:</span> <span className="font-bold text-yellow-400">{baselineResult.co2_g.toFixed(4)}g</span></p>
                      <p className="text-sm"><span className="text-gray-400">Latency:</span> <span className="font-bold text-yellow-400">{baselineResult.latency_ms}ms</span></p>
                    </div>
                  </div>
                  <div>
                    <h3 className="font-bold text-lg mb-3 text-accent">✨ CAMAS</h3>
                    <div className="bg-gray-900 border border-accent/30 rounded-lg p-4 space-y-2">
                      <p className="text-sm"><span className="text-gray-400">Model:</span> <span className="font-bold text-accent">{camasResult.model}</span></p>
                      <p className="text-sm"><span className="text-gray-400">Complexity:</span> <span className="font-bold text-accent">{camasResult.complexity.toFixed(1)}/10</span></p>
                      <p className="text-sm"><span className="text-gray-400">Energy:</span> <span className="font-bold text-green-400">{(camasResult.energy_kwh * 1000000).toFixed(2)} µkWh</span></p>
                      <p className="text-sm"><span className="text-gray-400">CO₂:</span> <span className="font-bold text-green-400">{camasResult.co2_g.toFixed(4)}g</span></p>
                      <p className="text-sm"><span className="text-gray-400">Latency:</span> <span className="font-bold text-green-400">{camasResult.latency_ms}ms</span></p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Single Result - CAMAS Only */}
            {camasResult && !baselineResult && (
              <div className="bg-gradient-to-br from-accent/15 to-accent/5 border border-accent/30 rounded-2xl p-8">
                <h2 className="text-2xl font-bold mb-6">✨ CAMAS Routing Result</h2>
                <div className="grid md:grid-cols-4 gap-4">
                  <div className="bg-gray-900/80 border border-accent/30 rounded-lg p-6 text-center">
                    <p className="text-accent text-2xl font-bold">{camasResult.model}</p>
                    <p className="text-gray-400 text-sm mt-2">Selected Model</p>
                  </div>
                  <div className="bg-gray-900/80 border border-accent/30 rounded-lg p-6 text-center">
                    <p className="text-accent text-2xl font-bold">{camasResult.complexity.toFixed(1)}</p>
                    <p className="text-gray-400 text-sm mt-2">Complexity</p>
                  </div>
                  <div className="bg-gray-900/80 border border-accent/30 rounded-lg p-6 text-center">
                    <p className="text-accent text-2xl font-bold">{(camasResult.energy_kwh * 1000000).toFixed(2)}</p>
                    <p className="text-gray-400 text-sm mt-2">Energy (µkWh)</p>
                  </div>
                  <div className="bg-gray-900/80 border border-accent/30 rounded-lg p-6 text-center">
                    <p className="text-accent text-2xl font-bold">{camasResult.co2_g.toFixed(4)}</p>
                    <p className="text-gray-400 text-sm mt-2">CO₂ (g)</p>
                  </div>
                </div>
                <div className="mt-6 bg-gray-900 border border-accent/30 rounded-lg p-4">
                  <p className="text-sm text-gray-300"><span className="text-accent font-bold">Routing Decision:</span> {camasResult.routing_reason}</p>
                </div>
              </div>
            )}

            {/* Single Result - Baseline Only */}
            {baselineResult && !camasResult && (
              <div className="bg-gradient-to-br from-yellow-900/15 to-yellow-800/5 border border-yellow-700/30 rounded-2xl p-8">
                <h2 className="text-2xl font-bold mb-6">⚙️ Baseline Result</h2>
                <div className="grid md:grid-cols-4 gap-4">
                  <div className="bg-gray-900/80 border border-yellow-600/30 rounded-lg p-6 text-center">
                    <p className="text-yellow-400 text-2xl font-bold">{baselineResult.model}</p>
                    <p className="text-gray-400 text-sm mt-2">Model (Always)</p>
                  </div>
                  <div className="bg-gray-900/80 border border-yellow-600/30 rounded-lg p-6 text-center">
                    <p className="text-yellow-400 text-2xl font-bold">{baselineResult.complexity.toFixed(1)}</p>
                    <p className="text-gray-400 text-sm mt-2">Complexity</p>
                  </div>
                  <div className="bg-gray-900/80 border border-yellow-600/30 rounded-lg p-6 text-center">
                    <p className="text-yellow-400 text-2xl font-bold">{(baselineResult.energy_kwh * 1000000).toFixed(2)}</p>
                    <p className="text-gray-400 text-sm mt-2">Energy (µkWh)</p>
                  </div>
                  <div className="bg-gray-900/80 border border-yellow-600/30 rounded-lg p-6 text-center">
                    <p className="text-yellow-400 text-2xl font-bold">{baselineResult.co2_g.toFixed(4)}</p>
                    <p className="text-gray-400 text-sm mt-2">CO₂ (g)</p>
                  </div>
                </div>
              </div>
            )}

            {/* Hint to run both */}
            {(camasResult || baselineResult) && !(camasResult && baselineResult) && (
              <div className="bg-blue-900/20 border border-blue-700/50 rounded-lg p-4">
                <p className="text-blue-300 text-sm">
                  💡 Run {camasResult ? 'Baseline' : 'CAMAS'} to see a comparison
                </p>
              </div>
            )}
          </div>
        )}

        {!baselineResult && !camasResult && !loading && (
          <div className="text-center py-12">
            <p className="text-xl text-gray-400">👆 Enter a query above and click a button to see results</p>
          </div>
        )}
      </div>
    </div>
  )
}
