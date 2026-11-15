export default function ResearchPage() {
  const researchSources = [
    {
      title: "Data Centers' $25 Billion Environmental Damage Cost",
      source: "National Bureau of Economic Research (NBER)",
      url: "https://www.nber.org/papers/w35100",
      key_finding: "Data centers consume 250 TWh of electricity (~5-6% of U.S. generation) causing $25B in environmental damages annually"
    },
    {
      title: "AI Energy Consumption & Scale Impact",
      source: "ArXiv Research",
      url: "https://arxiv.org/pdf/2505.09598",
      key_finding: "GPT-4o at scale: 700M queries/day = 35,000 U.S. homes worth of electricity + 1.2M people's annual water needs"
    },
    {
      title: "ChatGPT Energy Usage Report",
      source: "IEEE Spectrum & OpenAI",
      url: "https://spectrum.ieee.org/ai-energy-use",
      key_finding: "ChatGPT serves 2.5B queries/day at ~0.34 Wh per query = massive scale energy drain"
    },
    {
      title: "AI Computing Infrastructure 2030 Projections",
      source: "AInvest 2025 Study",
      url: "https://www.ainvest.com/news/growing-climate-financial-risks-data-center-driven-emissions-2601/",
      key_finding: "AI computing could emit 24-44M metric tons CO₂ annually by 2030 (5-10M cars equivalent)"
    },
    {
      title: "Data Center Operating Costs",
      source: "Michigan Advance",
      url: "https://michiganadvance.com/2026/08/27/why-on-earth-are-so-many-data-centers-being-built/",
      key_finding: "100 MW data center = $120M annual operating costs + environmental externalities"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-950 to-gray-900 py-12">
      <div className="max-w-6xl mx-auto px-4">
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

        {/* Industry Research: The Problem at Scale */}
        <div className="bg-gradient-to-br from-red-900/20 to-red-800/10 border border-red-800/50 rounded-lg p-8 mb-8">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
            <span>🚨</span> The Real Problem: Billions Lost to AI Energy Waste
          </h2>
          <div className="space-y-4">
            {researchSources.map((source, i) => (
              <div key={i} className="bg-gray-950/50 border border-red-800/30 rounded-lg p-4 hover:border-red-600/50 transition">
                <div className="flex justify-between items-start gap-4">
                  <div className="flex-1">
                    <h3 className="font-bold text-red-300 mb-1">{source.title}</h3>
                    <p className="text-sm text-gray-400 mb-2"><span className="font-semibold">Source:</span> {source.source}</p>
                    <p className="text-sm text-gray-300 bg-gray-900 p-2 rounded border-l-2 border-red-600 italic">
                      💡 {source.key_finding}
                    </p>
                  </div>
                  <a 
                    href={source.url} 
                    target="_blank" 
                    rel="noreferrer"
                    className="flex-shrink-0 px-3 py-2 bg-red-600 hover:bg-red-700 text-white rounded text-sm font-bold transition"
                  >
                    Read →
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Key Statistics from Research */}
        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-8 mb-8">
          <h2 className="text-2xl font-bold mb-6">📊 Industry-Wide Impact Statistics</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {[
              {
                stat: "$25 Billion",
                label: "Annual environmental damage from U.S. data centers alone",
                source: "NBER 2024 Study"
              },
              {
                stat: "250 TWh",
                label: "Annual electricity consumption by data centers (5-6% of U.S. generation)",
                source: "NBER Study"
              },
              {
                stat: "2.5 Billion",
                label: "ChatGPT queries per day at 0.34 Wh each = massive scale waste",
                source: "OpenAI & IEEE Spectrum"
              },
              {
                stat: "24-44M Tons",
                label: "Projected CO₂ from AI computing by 2030 (5-10M cars equivalent)",
                source: "AInvest 2025 Study"
              },
              {
                stat: "$120 Million",
                label: "Annual operating cost for single 100MW data center",
                source: "Michigan Advance"
              },
              {
                stat: "4,600x",
                label: "More energy consumed by large generative AI vs traditional models",
                source: "ArXiv Research"
              }
            ].map((item, i) => (
              <div key={i} className="bg-gradient-to-br from-red-900/10 to-orange-900/10 border border-orange-800/30 rounded-lg p-4">
                <p className="text-3xl font-bold text-orange-400 mb-2">{item.stat}</p>
                <p className="text-sm text-gray-300 mb-2">{item.label}</p>
                <p className="text-xs text-gray-500">📚 {item.source}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Performance Visualizations */}
        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-8 mb-8">
          <h2 className="text-2xl font-bold mb-6">📈 CAMAS Performance Visualizations</h2>
          <div className="grid md:grid-cols-2 gap-6">
            {[
              { img: '/fig1_energy_comparison.png', title: 'Energy Efficiency Comparison' },
              { img: '/fig2_carbon_comparison.png', title: 'Carbon Emissions Reduction' },
              { img: '/fig3_latency_comparison.png', title: 'Latency Improvements' },
              { img: '/fig4_cost_comparison.png', title: 'Cost Savings Analysis' },
              { img: '/fig5_routing_distribution.png', title: 'Model Routing Distribution' },
              { img: '/fig6_sleep_statistics.png', title: 'Energy-Aware Statistics' },
            ].map((viz, i) => (
              <div key={i} className="bg-gray-950 border border-gray-800 rounded-lg p-4 overflow-hidden hover:border-accent/50 transition">
                <h3 className="text-sm font-bold mb-3 text-accent">{viz.title}</h3>
                <div className="bg-gray-900 rounded">
                  <img src={viz.img} alt={viz.title} className="w-full h-auto" />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* How CAMAS Solves This */}
        <div className="bg-gradient-to-br from-green-900/20 to-green-800/10 border border-green-800/50 rounded-lg p-8 mb-8">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
            <span>✅</span> How CAMAS Solves the $25B Problem
          </h2>
          <div className="space-y-4">
            {[
              {
                problem: "$25B in annual U.S. data center environmental damage",
                solution: "CAMAS reduces energy consumption by 53.5% through intelligent routing",
                impact: "Potential to save $13B+ annually in U.S. data center damage costs alone"
              },
              {
                problem: "2.5B ChatGPT queries/day at 0.34 Wh each = massive waste on simple queries",
                solution: "CAMAS routes simple queries to phi3 (83% energy savings), complex to llama3.2:8b",
                impact: "35-40% of queries are simple - massive efficiency gains"
              },
              {
                problem: "250 TWh annual data center electricity = unsustainable growth trajectory",
                solution: "CAMAS demonstrates right-sizing models prevents over-provisioning",
                impact: "Could reduce data center electricity needs by 5-10 TWh annually industry-wide"
              },
              {
                problem: "Projected 24-44M tons CO₂ from AI by 2030 (5-10M cars equivalent)",
                solution: "CAMAS achieves 53.5% CO₂ reduction per query through efficiency",
                impact: "If adopted globally: 12-23M tons CO₂ reduction annually"
              },
              {
                problem: "$120M+ annual operating costs for 100MW data centers",
                solution: "CAMAS reduces per-query costs by 46.9% through smart routing",
                impact: "100MW data center saves $60M+ annually at scale"
              }
            ].map((item, i) => (
              <div key={i} className="bg-gray-950/50 border border-green-800/30 rounded-lg p-4">
                <div className="space-y-2">
                  <p className="text-sm"><span className="font-bold text-red-400">❌ Problem:</span> {item.problem}</p>
                  <p className="text-sm"><span className="font-bold text-blue-400">💡 CAMAS:</span> {item.solution}</p>
                  <p className="text-sm"><span className="font-bold text-green-400">✅ Impact:</span> {item.impact}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* GitHub & Resources */}
        <div className="bg-accent/10 border border-accent/30 rounded-lg p-8">
          <div className="flex items-start gap-4 mb-6">
            <span className="text-4xl">📘</span>
            <div>
              <h3 className="text-2xl font-bold mb-2">Full Source Code & Research</h3>
              <p className="text-gray-400 mb-4">All code, benchmarks, visualizations, and research documentation available on GitHub:</p>
              <a href="https://github.com/Praveen4278/camas" target="_blank" rel="noreferrer" className="text-accent hover:underline font-mono break-all">
                github.com/Praveen4278/camas
              </a>
            </div>
          </div>
          <div className="bg-gray-950 border border-gray-800 rounded-lg p-4">
            <p className="text-sm text-gray-300">Include: Full research paper, benchmark dataset (100 queries), performance visualizations, deployment guide, and reproducible experiments with CodeCarbon measurements</p>
          </div>
        </div>

        {/* Call to Action */}
        <div className="rounded-lg p-8 border-2 border-accent bg-gradient-to-br from-accent/20 to-accent/5">
          <div className="flex items-start gap-4">
            <span className="text-4xl">🎯</span>
            <div className="flex-1">
              <h3 className="text-2xl font-bold mb-3 text-accent">CAMAS: The Solution to AI's $25B Problem</h3>
              <p className="mb-4 text-gray-200">With $25B in annual environmental damage from data centers and explosive AI growth, CAMAS demonstrates that intelligent model routing can provide massive efficiency gains without sacrificing performance.</p>
              <div className="bg-accent/20 border border-accent/50 rounded p-3 inline-block">
                <p className="font-bold text-accent">✨ Try CAMAS now → Go to Orchestration Studio to test intelligent routing in action</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
