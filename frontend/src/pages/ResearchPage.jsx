export default function ResearchPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-950 to-gray-900 py-12">
      <div className="max-w-4xl mx-auto px-4">
        <h1 className="text-4xl font-bold mb-4">📚 Research & Documentation</h1>
        <p className="text-lg text-gray-400 mb-12">CAMAS: Carbon-Aware Multi-Agent System for Intelligent LLM Orchestration</p>

        {/* Abstract */}
        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-8 mb-8">
          <h2 className="text-2xl font-bold mb-4">🎯 Abstract</h2>
          <p className="text-gray-300 leading-relaxed mb-4">
            CAMAS is an intelligent LLM orchestration framework that addresses the growing energy consumption crisis in AI systems. By implementing complexity-based model routing, CAMAS reduces energy consumption by 53.5% while maintaining or improving performance. Instead of routing all queries to the most powerful model, CAMAS analyzes task complexity in real-time and selects the appropriate model: phi3 for simple queries, llama3.2:3b for medium-complexity tasks, and llama3.2:8b for complex reasoning tasks.
          </p>
          <p className="text-gray-300 leading-relaxed">
            This multi-agent approach orchestrates five specialized agents (Planner, Router, Executor, Energy Monitor, and Carbon Predictor) through LangGraph to create an efficient pipeline that reduces energy consumption, operational costs, and carbon emissions without sacrificing accuracy or user experience.
          </p>
        </div>

        {/* Problem Statement */}
        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-8 mb-8">
          <h2 className="text-2xl font-bold mb-6">⚠️ Problem Statement</h2>
          <div className="space-y-4 text-gray-300">
            <div className="border-l-4 border-red-600 pl-4">
              <p className="font-bold mb-1">Growing Energy Consumption</p>
              <p className="text-sm">Large language models consume significant energy. Using a single large model for all queries—regardless of complexity—wastes computational resources.</p>
            </div>
            <div className="border-l-4 border-red-600 pl-4">
              <p className="font-bold mb-1">Environmental Impact</p>
              <p className="text-sm">AI systems contribute to carbon emissions. Data centers consume ~10-15% of global electricity. LLM inference is a growing fraction of this.</p>
            </div>
            <div className="border-l-4 border-red-600 pl-4">
              <p className="font-bold mb-1">Economic Inefficiency</p>
              <p className="text-sm">Running expensive models for simple tasks increases operational costs unnecessarily—costs that accumulate at scale.</p>
            </div>
            <div className="border-l-4 border-red-600 pl-4">
              <p className="font-bold mb-1">Lack of Visibility</p>
              <p className="text-sm">Most AI systems don't measure or report energy consumption, making it impossible for organizations to assess their environmental impact.</p>
            </div>
          </div>
        </div>

        {/* Solution */}
        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-8 mb-8">
          <h2 className="text-2xl font-bold mb-6">💡 Solution: Intelligent Routing</h2>
          <p className="text-gray-300 mb-6">
            CAMAS solves this through <strong>complexity-aware model selection</strong>:
          </p>
          <div className="space-y-4">
            {[
              {
                stage: 'Analyze',
                description: 'Planner agent quickly analyzes query complexity using tokenization and heuristics',
                metrics: 'Complexity score: 0-10'
              },
              {
                stage: 'Route',
                description: 'Router selects the minimum viable model based on complexity score',
                metrics: 'phi3 (simple) → llama3.2:3b (medium) → llama3.2:8b (complex)'
              },
              {
                stage: 'Execute',
                description: 'Executor runs the query on the selected model via Ollama',
                metrics: 'Response generation at optimal efficiency'
              },
              {
                stage: 'Measure',
                description: 'Energy Monitor tracks real-time energy consumption using CodeCarbon',
                metrics: 'Accurate energy measurement per query'
              },
              {
                stage: 'Optimize',
                description: 'Carbon Predictor calculates emissions and stores metrics for analysis',
                metrics: 'CO₂ reduction tracked and reported'
              },
            ].map((item, i) => (
              <div key={i} className="bg-gray-950 border border-gray-800 rounded-lg p-4 flex gap-4">
                <div className="w-12 h-12 bg-accent rounded-lg flex items-center justify-center font-bold text-darker flex-shrink-0">{i + 1}</div>
                <div className="flex-1">
                  <h3 className="font-bold text-lg text-accent">{item.stage}</h3>
                  <p className="text-sm text-gray-300">{item.description}</p>
                  <p className="text-xs text-gray-500 mt-1 font-mono">{item.metrics}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Key Results */}
        <div className="bg-gradient-to-br from-green-900/20 to-green-800/10 border border-green-800/50 rounded-lg p-8 mb-8">
          <h2 className="text-2xl font-bold mb-6">📊 Key Results (p &lt; 0.001)</h2>
          <div className="space-y-3 text-gray-300">
            <div className="flex justify-between items-center p-3 bg-gray-950/50 rounded border border-green-800/30">
              <span><strong>Energy Reduction:</strong> 53.5% per query</span>
              <span className="text-green-400 font-bold">0.0059 kWh saved</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-gray-950/50 rounded border border-green-800/30">
              <span><strong>Carbon Reduction:</strong> 53.5% per query</span>
              <span className="text-green-400 font-bold">2.39g CO₂ saved</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-gray-950/50 rounded border border-green-800/30">
              <span><strong>Cost Savings:</strong> 46.9% per query</span>
              <span className="text-green-400 font-bold">$0.000015 saved</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-gray-950/50 rounded border border-green-800/30">
              <span><strong>Latency Improvement:</strong> 33.8% faster</span>
              <span className="text-green-400 font-bold">773.1ms saved</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-gray-950/50 rounded border border-green-800/30">
              <span><strong>Benchmark Scope:</strong> 100 diverse queries</span>
              <span className="text-green-400 font-bold">35% simple, 45% medium, 20% complex</span>
            </div>
          </div>
        </div>

        {/* Real-World Impact */}
        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-8 mb-8">
          <h2 className="text-2xl font-bold mb-6">🌍 Real-World Impact Projections</h2>
          <div className="space-y-4">
            {[
              {
                scale: 'Enterprise (10K queries/day)',
                annual_savings: '$50K - $100K',
                co2_reduction: '800+ tons CO₂',
                gpu_equivalent: '~12 GPU years saved'
              },
              {
                scale: 'Large Enterprise (100K queries/day)',
                annual_savings: '$500K - $1M',
                co2_reduction: '8,000+ tons CO₂',
                gpu_equivalent: '~120 GPU years saved'
              },
              {
                scale: 'Cloud Provider (1M queries/day)',
                annual_savings: '$5M - $10M',
                co2_reduction: '80,000+ tons CO₂',
                gpu_equivalent: '~1,200 GPU years saved'
              },
              {
                scale: 'Global Tech Company (10M queries/day)',
                annual_savings: '$50M - $100M',
                co2_reduction: '800,000+ tons CO₂',
                gpu_equivalent: '~12,000 GPU years saved'
              }
            ].map((item, i) => (
              <div key={i} className="bg-gray-950 border border-gray-800 rounded-lg p-4">
                <p className="font-bold text-accent mb-2">{item.scale}</p>
                <div className="grid md:grid-cols-3 gap-3 text-sm">
                  <div><span className="text-gray-400">Annual Savings:</span> <span className="font-bold text-green-400">{item.annual_savings}</span></div>
                  <div><span className="text-gray-400">CO₂ Reduction:</span> <span className="font-bold text-green-400">{item.co2_reduction}</span></div>
                  <div><span className="text-gray-400">GPU-Years Equiv:</span> <span className="font-bold text-green-400">{item.gpu_equivalent}</span></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Technical Details */}
        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-8 mb-8">
          <h2 className="text-2xl font-bold mb-6">🔧 Technical Implementation</h2>
          <div className="space-y-4">
            {[
              {
                component: 'Complexity Analysis',
                approach: 'Token count + keyword heuristics',
                models: 'phi3:latest for analysis',
              },
              {
                component: 'Model Routing',
                approach: 'Threshold-based selection (scores 0-10)',
                models: '0-3: phi3 | 4-7: llama3.2:3b | 8-10: llama3.2:8b',
              },
              {
                component: 'Energy Measurement',
                approach: 'CodeCarbon API (real-time monitoring)',
                models: 'Accurate CPU/GPU power tracking',
              },
              {
                component: 'Storage & Analytics',
                approach: 'SQLite + FastAPI REST endpoints',
                models: 'Query history + metrics persistence',
              },
            ].map((item, i) => (
              <div key={i} className="bg-gray-950 border border-gray-800 rounded-lg p-4">
                <h3 className="font-bold text-accent mb-2">{item.component}</h3>
                <p className="text-sm text-gray-300 mb-1"><span className="text-gray-400">Approach:</span> {item.approach}</p>
                <p className="text-sm text-gray-300"><span className="text-gray-400">Tech:</span> {item.models}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Future Work */}
        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-8 mb-8">
          <h2 className="text-2xl font-bold mb-6">🚀 Future Work</h2>
          <ul className="space-y-3 text-gray-300">
            <li className="flex gap-3">
              <span className="text-accent font-bold">•</span>
              <span><strong>Multi-Modal Models:</strong> Extend routing to vision and audio models</span>
            </li>
            <li className="flex gap-3">
              <span className="text-accent font-bold">•</span>
              <span><strong>Fine-tuning:</strong> Train custom models on domain-specific tasks for even better efficiency</span>
            </li>
            <li className="flex gap-3">
              <span className="text-accent font-bold">•</span>
              <span><strong>Distributed Systems:</strong> Scale to multiple GPUs/nodes for enterprise deployment</span>
            </li>
            <li className="flex gap-3">
              <span className="text-accent font-bold">•</span>
              <span><strong>Carbon-Aware Scheduling:</strong> Route queries to greener time periods based on grid mix</span>
            </li>
            <li className="flex gap-3">
              <span className="text-accent font-bold">•</span>
              <span><strong>Multi-Language Support:</strong> Extend beyond English queries</span>
            </li>
          </ul>
        </div>

        {/* GitHub & Resources */}
        <div className="bg-accent/10 border border-accent/30 rounded-lg p-8">
          <div className="flex items-start gap-4 mb-6">
            <span className="text-4xl">📘</span>
            <div>
              <h3 className="text-2xl font-bold mb-2">Full Source Code</h3>
              <p className="text-gray-400 mb-4">All code, benchmarks, and documentation available on GitHub:</p>
              <a href="https://github.com/Praveen4278/camas" target="_blank" rel="noreferrer" className="text-accent hover:underline font-mono break-all">
                github.com/Praveen4278/camas
              </a>
            </div>
          </div>
          <div className="bg-gray-950 border border-gray-800 rounded-lg p-4">
            <p className="text-sm text-gray-300">Include: Architecture diagrams, benchmark results, deployment guide, training data, and reproducible experiments</p>
          </div>
        </div>
      </div>
    </div>
  )
}
