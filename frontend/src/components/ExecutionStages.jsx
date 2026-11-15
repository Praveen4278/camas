const stages = [
  { id: 1, name: 'Task Analyzed', desc: 'Query complexity estimated', icon: '✓' },
  { id: 2, name: 'Planner Activated', desc: 'Task profile generated', icon: '✓' },
  { id: 3, name: 'Models Evaluated', desc: 'Routing candidates assessed', icon: '✓' },
  { id: 4, name: 'Model Selected', desc: 'Optimal model chosen', icon: '✓' },
  { id: 5, name: 'Execution', desc: 'Query processed', icon: '✓' },
  { id: 6, name: 'Metrics Recorded', desc: 'Energy & carbon logged', icon: '✓' },
]

function ExecutionStagesForMode({ result, loading, mode, isActive }) {
  const getCompletedStages = () => {
    if (loading && isActive) return 2
    if (result) return 6
    return 0
  }

  const completed = getCompletedStages()

  return (
    <div className="mb-8">
      <h3 className="font-bold text-lg mb-6 capitalize">
        {mode === 'baseline' ? 'Baseline Routing' : 'CAMAS Carbon-Aware Routing'}
      </h3>

      <div className="space-y-3">
        {stages.map((stage, idx) => {
          const isCompleted = idx < completed
          const isCurrent = idx === completed && loading && isActive

          return (
            <div key={stage.id} className="flex items-start gap-4">
              <div className="flex-shrink-0 mt-1">
                {isCompleted ? (
                  <span className="text-accent text-2xl">✓</span>
                ) : isCurrent ? (
                  <span className="text-gray-400 text-xl animate-spin">⏱</span>
                ) : (
                  <div className="w-6 h-6 border-2 border-gray-700 rounded-full"></div>
                )}
              </div>
              <div className="flex-1">
                <p className={`font-semibold ${isCompleted ? 'text-white' : 'text-gray-400'}`}>
                  {stage.name}
                </p>
                <p className="text-sm text-gray-500">{stage.desc}</p>

                {/* Result Data */}
                {result && isCompleted && stage.id === 4 && (
                  <div className="mt-3 p-3 bg-gray-900/50 border border-gray-800 rounded text-sm">
                    <p>
                      <span className="text-gray-400">Model Selected: </span>
                      <span className="font-semibold text-accent">{result.model}</span>
                    </p>
                    {result.complexity && (
                      <p className="mt-1">
                        <span className="text-gray-400">Complexity: </span>
                        <span className="font-semibold">{result.complexity.toFixed(2)}</span>
                      </p>
                    )}
                  </div>
                )}

                {result && isCompleted && stage.id === 6 && (
                  <div className="mt-3 p-3 bg-gray-900/50 border border-gray-800 rounded text-sm">
                    <p>
                      <span>⚡</span>
                      <span className="text-gray-400"> Energy: </span>
                      <span className="font-semibold">{(result.energy_kwh * 1000000).toFixed(2)} µkWh</span>
                    </p>
                    <p className="mt-1">
                      <span className="text-gray-400">Carbon: </span>
                      <span className="font-semibold">{result.co2_g?.toFixed(4) || '0.0000'} g CO₂</span>
                    </p>
                    <p className="mt-1">
                      <span className="text-gray-400">Latency: </span>
                      <span className="font-semibold">{result.latency_ms?.toFixed(0) || 0} ms</span>
                    </p>
                  </div>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default function ExecutionStages({ baselineResult, camasResult, loading, activeMode }) {
  return (
    <div className="bg-gray-900/50 border border-gray-800 rounded-2xl p-8 mb-12">
      <h2 className="text-2xl font-bold mb-8">Orchestration Pipeline</h2>

      <div className="grid md:grid-cols-2 gap-12">
        <ExecutionStagesForMode
          result={baselineResult}
          loading={loading}
          mode="baseline"
          isActive={activeMode === 'baseline'}
        />
        <ExecutionStagesForMode
          result={camasResult}
          loading={loading}
          mode="camas"
          isActive={activeMode === 'camas'}
        />
      </div>

      {/* Routing Decision Explanation */}
      {(baselineResult?.routing_reason || camasResult?.routing_reason) && (
        <div className="mt-8 pt-8 border-t border-gray-800 grid md:grid-cols-2 gap-8">
          {baselineResult?.routing_reason && (
            <div className="bg-gray-900 border border-gray-800 rounded-lg p-4">
              <p className="text-sm font-semibold mb-2 text-gray-400">BASELINE ROUTING LOGIC</p>
              <p className="text-sm text-gray-300">{baselineResult.routing_reason}</p>
            </div>
          )}
          {camasResult?.routing_reason && (
            <div className="bg-gray-900 border border-accent/30 rounded-lg p-4 bg-accent/5">
              <p className="text-sm font-semibold mb-2 text-accent">CAMAS ROUTING LOGIC</p>
              <p className="text-sm text-gray-300">{camasResult.routing_reason}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
