import { Link } from 'react-router-dom'

export default function LandingPage() {
  const impactMetrics = [
    { label: 'Energy Reduction', value: '53.5%', icon: '⚡', desc: 'Less power consumption per query' },
    { label: 'Carbon Cut', value: '53.5%', icon: '🌍', desc: 'Reduced CO₂ emissions' },
    { label: 'Cost Savings', value: '46.9%', icon: '💰', desc: 'Operational cost reduction' },
    { label: 'Latency Improvement', value: '33.8%', icon: '⚙️', desc: 'Faster response times' },
  ]

  const models = [
    {
      title: 'Simple Tasks',
      model: 'phi3',
      params: '3.8B parameters',
      energy: '70% less energy',
      latency: '500-1000ms',
      examples: 'Definitions, simple questions, summaries',
      cost: '$0.0001/query',
    },
    {
      title: 'Medium Tasks',
      model: 'llama3.2:3b',
      params: '3.2B parameters',
      energy: '40% less energy',
      latency: '1500-2000ms',
      examples: 'Analysis, coding, detailed explanations',
      cost: '$0.0004/query',
    },
    {
      title: 'Complex Tasks',
      model: 'llama3.2:8b',
      params: '8B parameters',
      energy: 'Full capability',
      latency: '2500-3500ms',
      examples: 'Reasoning, architecture design, research',
      cost: '$0.0014/query',
    },
  ]

  return (
    <div className="overflow-hidden">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center px-4 bg-gradient-to-br from-gray-950 via-gray-950 to-gray-900">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-10 w-72 h-72 bg-accent rounded-full filter blur-3xl"></div>
          <div className="absolute bottom-20 right-10 w-72 h-72 bg-accent rounded-full filter blur-3xl" style={{opacity: 0.05}}></div>
        </div>

        <div className="relative max-w-5xl mx-auto text-center">
          <div className="inline-block mb-6 px-4 py-2 bg-gray-900 border border-gray-800 rounded-full">
            <span className="text-accent text-sm font-semibold">🏆 INNOVEX 2026 • PS04: Smart Cities & Sustainability</span>
          </div>

          <h1 className="text-6xl sm:text-7xl font-bold mb-6 leading-tight">
            Making AI <br />
            <span className="text-accent">Sustainable & Intelligent</span>
          </h1>

          <p className="text-xl sm:text-2xl text-gray-300 mb-4 font-light">
            CAMAS: Carbon-Aware Multi-Agent System
          </p>

          <p className="text-lg sm:text-xl text-gray-400 mb-12 max-w-3xl mx-auto">
            Intelligently orchestrates AI workloads by analyzing query complexity and routing to optimal models. Reduces energy by 53.5%, cuts carbon emissions, and saves costs—all without sacrificing quality.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
            <Link to="/studio" className="inline-flex items-center justify-center px-8 py-4 bg-accent text-darker font-bold rounded-lg hover:shadow-lg hover:shadow-accent/50 transition transform hover:scale-105">
              🚀 Launch Interactive Demo
              <span className="ml-2">→</span>
            </Link>
            <Link to="/architecture" className="inline-flex items-center justify-center px-8 py-4 border border-gray-700 text-white font-semibold rounded-lg hover:bg-gray-900 transition">
              📐 See Architecture
            </Link>
            <Link to="/benchmarks" className="inline-flex items-center justify-center px-8 py-4 border border-gray-700 text-white font-semibold rounded-lg hover:bg-gray-900 transition">
              📊 View Benchmarks
            </Link>
            <Link to="/research" className="inline-flex items-center justify-center px-8 py-4 border border-gray-700 text-white font-semibold rounded-lg hover:bg-gray-900 transition">
              📚 Read Research
            </Link>
            <Link to="/results" className="inline-flex items-center justify-center px-8 py-4 border border-gray-700 text-white font-semibold rounded-lg hover:bg-gray-900 transition">
              📈 View Results
            </Link>
          </div>

          {/* Key Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 bg-gray-900/50 border border-gray-800 rounded-2xl p-8 backdrop-blur">
            {impactMetrics.map((metric, i) => (
              <div key={i} className="text-center">
                <div className="text-4xl mb-2">{metric.icon}</div>
                <div className="text-3xl font-bold text-accent mb-2">{metric.value}</div>
                <div className="text-xs sm:text-sm text-gray-400 font-semibold">{metric.label}</div>
                <div className="text-xs text-gray-500 mt-1">{metric.desc}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* The Problem Section */}
      <section className="py-24 px-4 bg-gray-900/50 border-t border-gray-800">
        <div className="max-w-5xl mx-auto">
          <div className="mb-8">
            <span className="text-accent font-bold text-sm">❌ THE CURRENT PROBLEM</span>
            <h2 className="text-4xl sm:text-5xl font-bold mt-3 mb-8">Why Today's AI is Wasteful</h2>
          </div>

          <div className="grid md:grid-cols-2 gap-8 mb-12">
            <div className="bg-gray-800/50 border border-red-500/30 rounded-xl p-8">
              <h3 className="text-xl font-bold text-red-400 mb-4">❌ Baseline Approach</h3>
              <ul className="space-y-3 text-gray-300">
                <li className="flex items-start gap-3">
                  <span className="text-red-400 mt-1">•</span>
                  <span>Routes ALL queries to 8B parameter model</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-red-400 mt-1">•</span>
                  <span>Simple "What is X?" uses full compute power</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-red-400 mt-1">•</span>
                  <span>50% computational resources wasted</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-red-400 mt-1">•</span>
                  <span>Massive energy & carbon footprint</span>
                </li>
              </ul>
            </div>

            <div className="bg-gray-800/50 border border-accent/30 rounded-xl p-8">
              <h3 className="text-xl font-bold text-accent mb-4">✅ CAMAS Approach</h3>
              <ul className="space-y-3 text-gray-300">
                <li className="flex items-start gap-3">
                  <span className="text-accent mt-1">•</span>
                  <span>Analyzes query complexity in milliseconds</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-accent mt-1">•</span>
                  <span>Routes to RIGHT-SIZED model for the task</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-accent mt-1">•</span>
                  <span>Optimal performance with minimal resources</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-accent mt-1">•</span>
                  <span>53.5% less energy, same quality output</span>
                </li>
              </ul>
            </div>
          </div>

          <div className="bg-accent/10 border border-accent/30 rounded-xl p-8 text-center">
            <p className="text-lg text-gray-300">
              <span className="font-bold text-accent">At Scale:</span> For 1 million queries/day in the cloud, CAMAS saves <span className="text-accent font-bold">$5-10M annually</span> and reduces CO₂ by <span className="text-accent font-bold">80,000+ tons/year</span>
            </p>
          </div>
        </div>
      </section>

      {/* The Solution Section */}
      <section className="py-24 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="mb-12">
            <span className="text-accent font-bold text-sm">✅ OUR SOLUTION</span>
            <h2 className="text-4xl sm:text-5xl font-bold mt-3 mb-4">Intelligent Model Routing</h2>
            <p className="text-gray-400 text-lg">CAMAS analyzes query complexity and routes to the optimal model—every single time.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {models.map((item, i) => (
              <div key={i} className="bg-gray-900 border border-gray-800 rounded-xl p-6 hover:border-accent/50 transition hover:shadow-lg hover:shadow-accent/10">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-bold text-xl">{item.title}</h3>
                  <span className="text-3xl">
                    {i === 0 ? '💨' : i === 1 ? '⚙️' : '🔋'}
                  </span>
                </div>

                <div className="space-y-2 mb-6 pb-6 border-b border-gray-800">
                  <p className="text-accent font-semibold">{item.model}</p>
                  <p className="text-sm text-gray-400">{item.params}</p>
                </div>

                <div className="space-y-3 text-sm">
                  <div>
                    <p className="text-gray-400">⚡ Energy</p>
                    <p className="font-bold text-accent">{item.energy}</p>
                  </div>
                  <div>
                    <p className="text-gray-400">⏱️ Latency</p>
                    <p className="font-bold">{item.latency}</p>
                  </div>
                  <div>
                    <p className="text-gray-400">💸 Cost/Query</p>
                    <p className="font-bold text-accent">{item.cost}</p>
                  </div>
                  <div className="pt-3 border-t border-gray-800">
                    <p className="text-gray-400 text-xs mb-2">Best for:</p>
                    <p className="text-gray-300">{item.examples}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-12 bg-gradient-to-r from-accent/10 via-gray-900 to-accent/10 border border-accent/30 rounded-xl p-8 text-center">
            <h3 className="text-2xl font-bold mb-3">Real-World Impact</h3>
            <p className="text-gray-300 mb-6">
              Using CAMAS instead of always-heavy baseline:
            </p>
            <div className="grid md:grid-cols-3 gap-6">
              <div>
                <p className="text-accent font-bold text-2xl">$50-100K</p>
                <p className="text-sm text-gray-400">Annual savings (10K queries/day)</p>
              </div>
              <div>
                <p className="text-accent font-bold text-2xl">800+ tons</p>
                <p className="text-sm text-gray-400">CO₂ reduction (10K queries/day)</p>
              </div>
              <div>
                <p className="text-accent font-bold text-2xl">2.5x ROI</p>
                <p className="text-sm text-gray-400">Infrastructure cost reduction</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-24 px-4 bg-gray-900/30 border-t border-gray-800">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-4xl font-bold mb-12 text-center">How CAMAS Works</h2>
          <div className="grid md:grid-cols-4 gap-6">
            {[
              { num: '1', title: 'Receive Query', desc: 'User submits AI task' },
              { num: '2', title: 'Analyze', desc: 'Measure task complexity' },
              { num: '3', title: 'Route', desc: 'Select optimal model' },
              { num: '4', title: 'Execute', desc: 'Process efficiently' },
            ].map((step, i) => (
              <div key={i} className="bg-gray-900 border border-gray-800 rounded-lg p-6 text-center">
                <div className="w-12 h-12 bg-accent text-darker font-bold rounded-full flex items-center justify-center mx-auto mb-4 text-lg">
                  {step.num}
                </div>
                <h3 className="font-bold mb-2">{step.title}</h3>
                <p className="text-gray-400 text-sm">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-6">See It In Action</h2>
          <p className="text-gray-400 text-lg mb-8">
            Try CAMAS with any query and see how it intelligently routes to the perfect model.
          </p>
          <Link to="/studio" className="inline-flex items-center justify-center px-8 py-4 bg-accent text-darker font-bold rounded-lg hover:shadow-lg hover:shadow-accent/50 transition transform hover:scale-105 text-lg">
            Launch Demo Now
            <span className="ml-2">→</span>
          </Link>
        </div>
      </section>
    </div>
  )
}
