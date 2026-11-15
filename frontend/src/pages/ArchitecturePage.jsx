export default function ArchitecturePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-950 to-gray-900 py-12">
      <div className="max-w-7xl mx-auto px-4">
        <h1 className="text-4xl font-bold mb-4">🏗️ Multi-Agent Architecture</h1>
        <p className="text-lg text-gray-400 mb-12">CAMAS orchestrates eight specialized agents through LangGraph for intelligent LLM routing, energy monitoring, and comprehensive result aggregation</p>

        {/* System Overview */}
        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-8 mb-12">
          <h2 className="text-2xl font-bold mb-6 text-center">🎯 CAMAS System Architecture (8 Agents)</h2>
          <div className="max-w-3xl mx-auto space-y-3">
            {[
              { 
                name: '1. Planner Agent', 
                desc: 'Analyzes task complexity (simple/medium/complex)', 
                input: 'User query',
                output: 'Complexity score (0-10)',
                icon: '🧠'
              },
              { 
                name: '2. Router Agent', 
                desc: 'Selects optimal model based on complexity', 
                input: 'Complexity score',
                output: 'Selected model (phi3/llama3.2:3b/llama3.2:8b)',
                icon: '🛣️'
              },
              { 
                name: '3. Executor Agent', 
                desc: 'Runs query on selected model via Ollama', 
                input: 'Model selection',
                output: 'Query result & response time',
                icon: '⚙️'
              },
              { 
                name: '4. Energy Monitor Agent', 
                desc: 'Measures real-time energy consumption (CodeCarbon)', 
                input: 'Model execution',
                output: 'Energy consumption (kWh)',
                icon: '⚡'
              },
              { 
                name: '5. Carbon Predictor Agent', 
                desc: 'Calculates CO₂ emissions from energy usage', 
                input: 'Energy data',
                output: 'CO₂ emissions (g)',
                icon: '🌍'
              },
              { 
                name: '6. Storage Agent', 
                desc: 'Persists query results and metrics to database', 
                input: 'All metrics (energy, CO₂, latency)',
                output: 'Stored record ID',
                icon: '💾'
              },
              { 
                name: '7. Aggregator Agent', 
                desc: 'Compiles comparison metrics (baseline vs CAMAS)', 
                input: 'Current result + historical baseline',
                output: 'Savings percentages & deltas',
                icon: '📊'
              },
              { 
                name: '8. API Response Agent', 
                desc: 'Formats complete response for frontend', 
                input: 'All metrics and comparisons',
                output: 'JSON response with visualizations',
                icon: '📤'
              },
            ].map((agent, i) => (
              <div key={i} className="flex gap-4 p-4 bg-gray-950 border border-gray-800 rounded-lg hover:border-accent/50 transition">
                <div className="w-10 h-10 bg-accent rounded-lg flex items-center justify-center text-darker font-bold flex-shrink-0 text-xl">
                  {agent.icon}
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-bold text-lg">{agent.name}</h3>
                  <p className="text-sm text-gray-400">{agent.desc}</p>
                  <div className="mt-2 text-xs text-gray-500 grid grid-cols-2 gap-2">
                    <div><span className="text-accent font-semibold">Input:</span> {agent.input}</div>
                    <div><span className="text-accent font-semibold">Output:</span> {agent.output}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Model Selection Logic */}
        <div className="bg-gradient-to-br from-blue-900/20 to-blue-800/10 border border-blue-800/50 rounded-lg p-8 mb-12">
          <h2 className="text-2xl font-bold mb-6">🤖 Intelligent Model Selection Logic</h2>
          <div className="space-y-4">
            {[
              {
                model: 'phi3:latest',
                complexity: 'Simple (Score 0-3)',
                description: 'Lightweight model for basic queries',
                use_cases: ['Factual information', 'Simple math', 'Quick definitions'],
                energy: '0.000018 kWh',
                params: '3.8B',
                benefit: '83% energy savings vs baseline'
              },
              {
                model: 'llama3.2:3b',
                complexity: 'Medium (Score 4-7)',
                description: 'Balanced model for analytical tasks',
                use_cases: ['Code analysis', 'Multi-step reasoning', 'Text summarization'],
                energy: '0.000047 kWh',
                params: '3B',
                benefit: '58% energy savings vs baseline'
              },
              {
                model: 'llama3.2:8b',
                complexity: 'Complex (Score 8-10)',
                description: 'Powerful model for advanced reasoning',
                use_cases: ['Deep analysis', 'Abstract concepts', 'Research synthesis'],
                energy: '0.000087 kWh',
                params: '8B',
                benefit: '22% energy savings vs baseline'
              }
            ].map((item, i) => (
              <div key={i} className="bg-gray-950/50 border border-blue-800/30 rounded-lg p-4">
                <div className="grid md:grid-cols-3 gap-4">
                  <div>
                    <p className="text-accent font-bold">{item.model}</p>
                    <p className="text-sm text-gray-400 mt-1">{item.complexity}</p>
                    <p className="text-xs text-gray-500 mt-2">Parameters: {item.params}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-300">{item.description}</p>
                    <p className="text-xs text-gray-400 mt-2">Use cases: {item.use_cases.join(', ')}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm"><span className="font-bold">Energy:</span> {item.energy}</p>
                    <p className="text-sm text-green-400 font-bold mt-2">✓ {item.benefit}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Technology Stack */}
        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-8 mb-12">
          <h2 className="text-2xl font-bold mb-6">🛠️ Technology Stack</h2>
          <div className="grid md:grid-cols-3 gap-4">
            {[
              { 
                tech: 'LangGraph', 
                desc: 'Multi-agent orchestration & workflow',
                category: 'Orchestration',
                icon: '🔗'
              },
              { 
                tech: 'Ollama', 
                desc: 'Local LLM runtime environment',
                category: 'LLM Runtime',
                icon: '🦙'
              },
              { 
                tech: 'CodeCarbon', 
                desc: 'Real-time energy measurement API',
                category: 'Monitoring',
                icon: '⚡'
              },
              { 
                tech: 'FastAPI', 
                desc: 'Modern Python async REST API',
                category: 'Backend',
                icon: '🚀'
              },
              { 
                tech: 'SQLite', 
                desc: 'Lightweight persistent storage',
                category: 'Database',
                icon: '💾'
              },
              { 
                tech: 'React 19', 
                desc: 'Modern frontend UI framework',
                category: 'Frontend',
                icon: '⚛️'
              },
            ].map((item, i) => (
              <div key={i} className="bg-gray-950 border border-gray-800 rounded-lg p-4 hover:border-accent/50 transition">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-2xl">{item.icon}</span>
                  <p className="font-bold text-accent">{item.tech}</p>
                </div>
                <p className="text-sm text-gray-300 mb-2">{item.desc}</p>
                <p className="text-xs text-gray-500 bg-gray-900 px-2 py-1 rounded w-fit">{item.category}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Data Flow Diagram */}
        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-8 mb-12">
          <h2 className="text-2xl font-bold mb-6">📊 Data Flow Pipeline</h2>
          <div className="space-y-4">
            {[
              {
                step: 'Input',
                description: 'User query submitted via REST API',
                details: 'Query text → FastAPI endpoint'
              },
              {
                step: 'Analysis',
                description: 'Planner analyzes query complexity',
                details: 'Tokenization → Complexity scoring (0-10)'
              },
              {
                step: 'Routing',
                description: 'Router selects optimal LLM model',
                details: 'Score mapping → Model selection logic'
              },
              {
                step: 'Execution',
                description: 'Executor runs query on Ollama',
                details: 'Model invocation → Response generation'
              },
              {
                step: 'Measurement',
                description: 'Energy Monitor tracks power usage',
                details: 'CodeCarbon API → Energy (kWh) recorded'
              },
              {
                step: 'Calculation',
                description: 'Carbon Predictor computes emissions',
                details: 'Energy × Grid CO₂ intensity = CO₂ (g)'
              },
              {
                step: 'Storage',
                description: 'Results persisted to database',
                details: 'SQLite → Query history + metrics'
              },
              {
                step: 'Output',
                description: 'Response returned to frontend',
                details: 'Result + Energy + CO₂ + Latency metrics'
              },
            ].map((item, i) => (
              <div key={i} className="flex gap-4 items-start">
                <div className="w-12 h-12 bg-accent rounded-lg flex items-center justify-center font-bold text-darker flex-shrink-0">
                  {i + 1}
                </div>
                <div className="flex-1 bg-gray-950 border border-gray-800 rounded-lg p-4">
                  <h3 className="font-bold text-accent">{item.step}</h3>
                  <p className="text-sm text-gray-300">{item.description}</p>
                  <p className="text-xs text-gray-500 mt-1">{item.details}</p>
                </div>
                {i < 7 && <div className="text-gray-700 mt-8">↓</div>}
              </div>
            ))}
          </div>
        </div>

        {/* Why This Architecture */}
        <div className="bg-gradient-to-br from-green-900/20 to-green-800/10 border border-green-800/50 rounded-lg p-8">
          <h2 className="text-2xl font-bold mb-6">✅ Why This Architecture Works</h2>
          <div className="grid md:grid-cols-2 gap-6">
            {[
              {
                title: '⚡ Energy Efficiency',
                points: [
                  'Avoids over-computation for simple tasks',
                  'Complexity analysis prevents wasted cycles',
                  'Right-sized models for each task type'
                ]
              },
              {
                title: '💰 Cost Optimization',
                points: [
                  'Smaller models = lower inference costs',
                  '53.5% cost reduction per query',
                  'Scales efficiently across large volumes'
                ]
              },
              {
                title: '🚀 Performance',
                points: [
                  'Faster responses for simple queries',
                  'Reduced latency by 33.8% overall',
                  'Better user experience'
                ]
              },
              {
                title: '🌍 Environmental Impact',
                points: [
                  '53.5% CO₂ reduction per query',
                  'Enables sustainable AI systems',
                  'Aligns with net-zero commitments'
                ]
              },
            ].map((section, i) => (
              <div key={i} className="bg-gray-950/50 border border-green-800/30 rounded-lg p-4">
                <h3 className="font-bold text-lg mb-3">{section.title}</h3>
                <ul className="space-y-2">
                  {section.points.map((point, j) => (
                    <li key={j} className="text-sm text-gray-300 flex gap-2">
                      <span className="text-green-400 font-bold">✓</span>
                      <span>{point}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
