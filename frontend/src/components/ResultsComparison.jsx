import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts'

export default function ResultsComparison({ baseline, camas }) {
  // Calculate improvements
  const energyReduction = ((baseline.energy_kwh - camas.energy_kwh) / baseline.energy_kwh * 100).toFixed(1)
  const carbonReduction = ((baseline.co2_g - camas.co2_g) / baseline.co2_g * 100).toFixed(1)
  const costReduction = ((baseline.cost_usd - camas.cost_usd) / baseline.cost_usd * 100).toFixed(1)
  const latencyImprovement = ((baseline.latency_ms - camas.latency_ms) / baseline.latency_ms * 100).toFixed(1)

  // Chart data
  const energyData = [
    { name: 'Baseline', value: (baseline.energy_kwh * 1000000).toFixed(2) },
    { name: 'CAMAS', value: (camas.energy_kwh * 1000000).toFixed(2) },
  ]

  const latencyData = [
    { name: 'Baseline', value: baseline.latency_ms?.toFixed(0) || 0 },
    { name: 'CAMAS', value: camas.latency_ms?.toFixed(0) || 0 },
  ]

  const costData = [
    { name: 'Baseline', value: (baseline.cost_usd * 1000000).toFixed(2) },
    { name: 'CAMAS', value: (camas.cost_usd * 1000000).toFixed(2) },
  ]

  const metrics = [
    {
      label: 'Energy Reduction',
      value: `${energyReduction}%`,
      icon: '⚡',
      color: 'text-yellow-400',
      bgColor: 'bg-yellow-500/10',
      borderColor: 'border-yellow-500/30',
    },
    {
      label: 'Carbon Cut',
      value: `${carbonReduction}%`,
      icon: '🌱',
      color: 'text-green-400',
      bgColor: 'bg-green-500/10',
      borderColor: 'border-green-500/30',
    },
    {
      label: 'Latency Improvement',
      value: `${latencyImprovement}%`,
      icon: '⏱️',
      color: 'text-blue-400',
      bgColor: 'bg-blue-500/10',
      borderColor: 'border-blue-500/30',
    },
    {
      label: 'Cost Savings',
      value: `${costReduction}%`,
      icon: '💰',
      color: 'text-accent',
      bgColor: 'bg-accent/10',
      borderColor: 'border-accent/30',
    },
  ]

  return (
    <div className="space-y-8">
      {/* Results Header */}
      <div className="flex items-center gap-3 mb-8">
        <span className="text-4xl">📉</span>
        <div>
          <h2 className="text-3xl font-bold">Comparison Results</h2>
          <p className="text-gray-400">How CAMAS optimizes compared to baseline routing</p>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
        {metrics.map((metric, i) => {
          return (
            <div
              key={i}
              className={`${metric.bgColor} border ${metric.borderColor} rounded-lg p-6 hover:border-accent/50 transition`}
            >
              <span className="text-3xl mb-3 block">{metric.icon}</span>
              <p className="text-gray-400 text-sm mb-2">{metric.label}</p>
              <p className={`text-2xl font-bold ${metric.color}`}>{metric.value}</p>
            </div>
          )
        })}
      </div>

      {/* Detailed Metrics Table */}
      <div className="bg-gray-900/50 border border-gray-800 rounded-2xl p-8 overflow-x-auto">
        <h3 className="font-bold text-lg mb-6">Detailed Metrics</h3>
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-800">
              <th className="text-left py-3 px-4 font-semibold">Metric</th>
              <th className="text-right py-3 px-4 font-semibold">Baseline</th>
              <th className="text-right py-3 px-4 font-semibold">CAMAS</th>
              <th className="text-right py-3 px-4 font-semibold">Improvement</th>
            </tr>
          </thead>
          <tbody>
            <tr className="border-b border-gray-800/50 hover:bg-gray-800/20">
              <td className="py-3 px-4">Energy</td>
              <td className="text-right py-3 px-4">{(baseline.energy_kwh * 1000000).toFixed(2)} µkWh</td>
              <td className="text-right py-3 px-4">{(camas.energy_kwh * 1000000).toFixed(2)} µkWh</td>
              <td className="text-right py-3 px-4 text-accent font-semibold">↓ {energyReduction}%</td>
            </tr>
            <tr className="border-b border-gray-800/50 hover:bg-gray-800/20">
              <td className="py-3 px-4">Carbon Emissions</td>
              <td className="text-right py-3 px-4">{baseline.co2_g?.toFixed(6) || '0.000000'} g</td>
              <td className="text-right py-3 px-4">{camas.co2_g?.toFixed(6) || '0.000000'} g</td>
              <td className="text-right py-3 px-4 text-accent font-semibold">↓ {carbonReduction}%</td>
            </tr>
            <tr className="border-b border-gray-800/50 hover:bg-gray-800/20">
              <td className="py-3 px-4">Latency</td>
              <td className="text-right py-3 px-4">{baseline.latency_ms?.toFixed(0) || 0} ms</td>
              <td className="text-right py-3 px-4">{camas.latency_ms?.toFixed(0) || 0} ms</td>
              <td className="text-right py-3 px-4 text-accent font-semibold">↓ {latencyImprovement}%</td>
            </tr>
            <tr className="border-b border-gray-800/50 hover:bg-gray-800/20">
              <td className="py-3 px-4">Cost</td>
              <td className="text-right py-3 px-4">${baseline.cost_usd?.toFixed(8) || '0.00000000'}</td>
              <td className="text-right py-3 px-4">${camas.cost_usd?.toFixed(8) || '0.00000000'}</td>
              <td className="text-right py-3 px-4 text-accent font-semibold">↓ {costReduction}%</td>
            </tr>
            <tr className="hover:bg-gray-800/20">
              <td className="py-3 px-4">Model Used</td>
              <td className="text-right py-3 px-4 font-mono text-sm">{baseline.model}</td>
              <td className="text-right py-3 px-4 font-mono text-sm">{camas.model}</td>
              <td className="text-right py-3 px-4">
                <span className="inline-block bg-accent/20 text-accent px-2 py-1 rounded text-xs font-semibold">
                  Right-sized
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Charts */}
      <div className="grid md:grid-cols-3 gap-8">
        {/* Energy Chart */}
        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-6">
          <h4 className="font-semibold mb-4">Energy Usage (µkWh)</h4>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={energyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="name" stroke="#999" />
              <YAxis stroke="#999" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1a1a1a',
                  border: '1px solid #333',
                  borderRadius: '8px',
                }}
                formatter={(value) => `${parseFloat(value).toFixed(2)} µkWh`}
              />
              <Bar dataKey="value" fill="#00ff88" radius={[8, 8, 0, 0]}>
                {energyData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={index === 0 ? '#666' : '#00ff88'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Latency Chart */}
        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-6">
          <h4 className="font-semibold mb-4">Latency (ms)</h4>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={latencyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="name" stroke="#999" />
              <YAxis stroke="#999" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1a1a1a',
                  border: '1px solid #333',
                  borderRadius: '8px',
                }}
                formatter={(value) => `${parseFloat(value).toFixed(0)} ms`}
              />
              <Bar dataKey="value" fill="#00ff88" radius={[8, 8, 0, 0]}>
                {latencyData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={index === 0 ? '#666' : '#00ff88'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Cost Chart */}
        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-6">
          <h4 className="font-semibold mb-4">Cost (µ$)</h4>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={costData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="name" stroke="#999" />
              <YAxis stroke="#999" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1a1a1a',
                  border: '1px solid #333',
                  borderRadius: '8px',
                }}
                formatter={(value) => `$${(parseFloat(value) / 1000000).toFixed(8)}`}
              />
              <Bar dataKey="value" fill="#00ff88" radius={[8, 8, 0, 0]}>
                {costData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={index === 0 ? '#666' : '#00ff88'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Response Display */}
      <div className="grid md:grid-cols-2 gap-8">
        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-6">
          <h4 className="font-semibold mb-4">Baseline Response</h4>
          <div className="bg-gray-950 p-4 rounded border border-gray-800 text-sm text-gray-300 max-h-40 overflow-y-auto">
            {baseline.response || 'No response generated'}
          </div>
        </div>
        <div className="bg-gray-900/50 border border-accent/30 rounded-lg p-6 bg-accent/5">
          <h4 className="font-semibold mb-4 text-accent">CAMAS Response</h4>
          <div className="bg-gray-950 p-4 rounded border border-accent/20 text-sm text-gray-300 max-h-40 overflow-y-auto">
            {camas.response || 'No response generated'}
          </div>
        </div>
      </div>
    </div>
  )
}
