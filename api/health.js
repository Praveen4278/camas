// Health check endpoint for CAMAS API

export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.status(200).json({
    status: 'healthy',
    service: 'CAMAS API',
    timestamp: Date.now()
  });
}
