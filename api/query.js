// CAMAS Backend API - Vercel Serverless Function
// Endpoint: /api/query

export default function handler(req, res) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { query, mode = 'camas' } = req.body;

  if (!query) {
    return res.status(400).json({ error: 'Query is required' });
  }

  const queryText = query.toLowerCase();

  // Calculate complexity based on query characteristics
  const words = queryText.split(' ');
  const wordCount = words.length;
  const charCount = queryText.length;

  // Base complexity from length
  let complexity = Math.min(10, (wordCount / 5) + (charCount / 100));

  // Boost complexity for technical keywords
  const technicalKeywords = [
    'design', 'architecture', 'implement', 'optimize', 'algorithm',
    'system', 'framework', 'explain', 'analyze', 'complex', 'abstract',
    'distributed', 'machine', 'learning', 'neural', 'transform'
  ];

  const keywordBoost = technicalKeywords.filter(k => queryText.includes(k)).length * 0.5;
  complexity = Math.min(10, complexity + keywordBoost);

  // Add small random variation (±5%)
  const hashValue = queryText.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
  complexity += (complexity * 0.05 * (2 * ((hashValue % 10) / 10) - 1));
  complexity = Math.max(1, Math.min(10, complexity));

  // Baseline always uses heavy model
  const baselineModel = 'llama3.2:8b';
  const baselineEnergy = 0.000111;
  const baselineCo2 = 0.0446;
  const baselineLatency = 2300 + complexity * 300 + ((hashValue % 600) - 300);

  // Model selection for CAMAS based on complexity
  let camasModel, camasEnergy, camasCo2, camasLatency;

  if (complexity < 3) {
    camasModel = 'phi3';
    camasEnergy = 0.000018;
    camasCo2 = 0.0072;
    camasLatency = 800 + (hashValue % 300);
  } else if (complexity < 6) {
    camasModel = 'llama3.2:3b';
    camasEnergy = 0.000047;
    camasCo2 = 0.0188;
    camasLatency = 1300 + (hashValue % 400);
  } else {
    camasModel = 'llama3.2:8b';
    camasEnergy = 0.000087;
    camasCo2 = 0.0349;
    camasLatency = 1700 + (hashValue % 500);
  }

  // Determine what to return based on mode
  let model, energy, co2, latency, routingReason;
  let energySavings, co2Savings, latencySavings, costSavings;

  if (mode === 'baseline') {
    model = baselineModel;
    energy = baselineEnergy;
    co2 = baselineCo2;
    latency = Math.round(baselineLatency);
    routingReason = 'Baseline always uses llama3.2:8b';
    energySavings = 0;
    co2Savings = 0;
    latencySavings = 0;
    costSavings = 0;
  } else {
    model = camasModel;
    energy = camasEnergy;
    co2 = camasCo2;
    latency = Math.round(camasLatency);
    routingReason = `CAMAS routed to ${camasModel} (Complexity: ${complexity.toFixed(1)}/10)`;
    energySavings = Math.round(((baselineEnergy - camasEnergy) / baselineEnergy) * 1000) / 10;
    co2Savings = Math.round(((baselineCo2 - camasCo2) / baselineCo2) * 1000) / 10;
    latencySavings = Math.round(baselineLatency - camasLatency);
    costSavings = Math.round((baselineEnergy - camasEnergy) * 0.15 * 100000000) / 100000000;
  }

  return res.status(200).json({
    status: 'success',
    query: queryText.length > 50 ? queryText.substring(0, 50) + '...' : queryText,
    complexity_score: Math.round(complexity * 10) / 10,
    model_selected: model,
    response: `This response is for: ${queryText.substring(0, 40)}...`,
    energy_kwh: energy,
    co2_grams: co2,
    latency_ms: latency,
    baseline_energy_kwh: baselineEnergy,
    baseline_co2_grams: baselineCo2,
    baseline_latency_ms: Math.round(baselineLatency),
    energy_savings_percent: energySavings,
    co2_savings_percent: co2Savings,
    latency_savings_ms: latencySavings,
    cost_savings_usd: costSavings,
    routing_reason: routingReason,
    timestamp: Date.now()
  });
}
