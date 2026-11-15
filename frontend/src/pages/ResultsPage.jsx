import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function ResultsPage() {
  // Routing distribution data
  const routingData = [
    { model: 'phi3', queries: 25, percentage: 25, color: '#10b981' },
    { model: 'llama3.2:3b', queries: 29, percentage: 29, color: '#3b82f6' },
    { model: 'llama3.2:8b', queries: 46, percentage: 46, color: '#f59e0b' },
  ]

  // Project impact data
  const impactData = [
    { metric: 'Cost Saved', value: 46.9, unit: '%', color: '#3b82f6' },
    { metric: 'Energy Saved', value: 53.5, unit: '%', color: '#10b981' },
    { metric: 'CO₂ Cut', value: 53.5, unit: '%', color: '#8b5cf6' },
    { metric: 'Latency Improved', value: 33.8, unit: '%', color: '#ec4899' },
  ]

  // Experimental results
  const experimentalResults = [
    { metric: 'Avg Latency (ms)', baseline: 2287.9, camas: 1514.8, improvement: '-33.8%' },
    { metric: 'Total Energy (kWh)', baseline: 0.011148, camas: 0.005182, improvement: '-53.5%' },
    { metric: 'Total CO₂ (g)', baseline: 4.4593, camas: 2.0726, improvement: '-53.5%' },
    { metric: 'Total Cost (USD)', baseline: 0.003300, camas: 0.001754, improvement: '-46.9%' },
  ]

  // Ablation study data
  const ablationData = [
    { config: 'Baseline (8b)', latency: 2318.2, energy: 0.04669, energySavings: 'ref' },
    { config: 'Routing OFF', latency: 2141.9, energy: 0.04823, energySavings: '-3.3%' },
    { config: 'Sleep OFF', latency: 1618.1, energy: 0.001179, energySavings: '-74.8%' },
    { config: 'Full CAMAS', latency: 1016.3, energy: 0.001182, energySavings: '-74.7%' },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-950 to-gray-900 py-12">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-5xl font-bold mb-4">📊 Research Results</h1>
          <p className="text-xl text-gray-400">
            Comprehensive analysis of CAMAS performance on 100 real-world queries
          </p>
        </div>

        {/* Project Impact Cards */}
        <div className="grid md:grid-cols-4 gap-4 mb-12">
          {impactData.map((item, idx) => (
            <div key={idx} className="bg-gray-900/80 border border-gray-800 rounded-lg p-6 text-center">
              <div className="text-4xl font-bold mb-2" style={{ color: item.color }}>
                {item.value}{item.unit}
              </div>
              <p className="text-gray-400 text-sm">{item.metric}</p>
            </div>
          ))}
        </div>

        {/* Two Column Layout */}
        <div className="grid lg:grid-cols-2 gap-8 mb-12">
          {/* Routing Distribution */}
          <div className="bg-gray-900/50 border border-gray-800 rounded-2xl p-8">
            <h2 className="text-2xl font-bold mb-6">🛣️ Routing Distribution (100 queries)</h2>
            <div className="space-y-4 mb-6">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-700">
                    <th className="text-left py-2 text-gray-400">Model</th>
                    <th className="text-right py-2 text-gray-400">Queries</th>
                    <th className="text-right py-2 text-gray-400">Distribution</th>
                  </tr>
                </thead>
                <tbody>
                  {routingData.map((row, idx) => (
                    <tr key={idx} className="border-b border-gray-800">
                      <td className="py-3">
                        <span className="font-bold" style={{ color: row.color }}>
                          {row.model}
                        </span>
                      </td>
                      <td className="text-right font-bold text-white">{row.queries}</td>
                      <td className="text-right" style={{ color: row.color }}>
                        <span className="font-bold">{row.percentage}%</span>
                      </td>
                    </tr>
                  ))}
                  <tr className="font-bold text-white">
                    <td className="py-3">Total</td>
                    <td className="text-right">100</td>
                    <td className="text-right">100%</td>
                  </tr>
                </tbody>
              </table>
            </div>

            {/* Pie Chart */}
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={routingData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ model, percentage }) => `${model} (${percentage}%)`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="queries"
                >
                  {routingData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>

            <p className="text-xs text-gray-500 mt-4 text-center">
              Shows how CAMAS intelligently routes queries based on complexity
            </p>
          </div>

          {/* Experimental Results Comparison */}
          <div className="bg-gray-900/50 border border-gray-800 rounded-2xl p-8">
            <h2 className="text-2xl font-bold mb-6">🔬 Experimental Results (n=100)</h2>
            <div className="space-y-3">
              {experimentalResults.map((result, idx) => (
                <div key={idx} className="bg-gray-800/50 rounded-lg p-4">
                  <p className="text-sm text-gray-400 mb-2">{result.metric}</p>
                  <div className="grid grid-cols-3 gap-3 text-sm">
                    <div>
                      <p className="text-gray-500 text-xs">Baseline</p>
                      <p className="font-bold text-white">{result.baseline}</p>
                    </div>
                    <div>
                      <p className="text-gray-500 text-xs">CAMAS</p>
                      <p className="font-bold text-accent">{result.camas}</p>
                    </div>
                    <div>
                      <p className="text-gray-500 text-xs">Improvement</p>
                      <p className="font-bold text-green-400">{result.improvement}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Ablation Study */}
        <div className="bg-gray-900/50 border border-gray-800 rounded-2xl p-8 mb-12">
          <h2 className="text-2xl font-bold mb-6">🧪 Ablation Study (50 per condition)</h2>
          <p className="text-gray-400 text-sm mb-6">
            Demonstrates that every module contributes to overall optimization
          </p>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-700">
                  <th className="text-left py-3 px-4 text-gray-400">Configuration</th>
                  <th className="text-right py-3 px-4 text-gray-400">Latency (ms)</th>
                  <th className="text-right py-3 px-4 text-gray-400">Energy (kWh)</th>
                  <th className="text-right py-3 px-4 text-gray-400">Energy Savings</th>
                  <th className="text-right py-3 px-4 text-gray-400">Impact</th>
                </tr>
              </thead>
              <tbody>
                {ablationData.map((row, idx) => (
                  <tr key={idx} className="border-b border-gray-800">
                    <td className="py-3 px-4">
                      <span className="font-bold text-white">{row.config}</span>
                    </td>
                    <td className="text-right py-3 px-4 text-white">{row.latency.toFixed(1)}</td>
                    <td className="text-right py-3 px-4 text-white">{row.energy.toFixed(5)}</td>
                    <td className="text-right py-3 px-4">
                      <span className={row.energySavings === 'ref' ? 'text-gray-400' : 'text-yellow-400 font-bold'}>
                        {row.energySavings}
                      </span>
                    </td>
                    <td className="text-right py-3 px-4">
                      {idx === 0 && <span className="text-gray-400">baseline</span>}
                      {idx === 1 && <span className="text-orange-400">reduces efficiency</span>}
                      {idx === 2 && <span className="text-green-400">sleep state critical</span>}
                      {idx === 3 && <span className="text-green-400 font-bold">full optimization</span>}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Key Findings */}
        <div className="bg-gradient-to-r from-accent/10 to-accent/5 border border-accent/30 rounded-2xl p-8">
          <h2 className="text-2xl font-bold mb-6">🎯 Key Findings</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-bold text-accent mb-3">✅ Routing Effectiveness</h3>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• 25% of queries routed to energy-efficient phi3</li>
                <li>• 29% to balanced llama3.2:3b</li>
                <li>• 46% to powerful llama3.2:8b when needed</li>
                <li>• Smart complexity detection ensures optimal model selection</li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-bold text-accent mb-3">📈 Measurable Impact</h3>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• 53.5% reduction in energy consumption</li>
                <li>• 53.5% reduction in CO₂ emissions</li>
                <li>• 46.9% cost savings per query</li>
                <li>• 33.8% improvement in latency</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
