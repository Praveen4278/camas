export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="border-t border-gray-800 bg-gray-950 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div>
            <h3 className="font-bold text-lg mb-4 text-accent">CAMAS</h3>
            <p className="text-gray-400 text-sm">
              Carbon-Aware Multi-Agent System. Making AI more sustainable.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-semibold mb-4">Product</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li>
                <a href="/studio" className="hover:text-accent transition">
                  Orchestration Studio
                </a>
              </li>
              <li>
                <a href="/dashboard" className="hover:text-accent transition">
                  Dashboard
                </a>
              </li>
              <li>
                <a href="/benchmarks" className="hover:text-accent transition">
                  Benchmarks
                </a>
              </li>
            </ul>
          </div>

          {/* Research */}
          <div>
            <h4 className="font-semibold mb-4">Research</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li>
                <a href="/research" className="hover:text-accent transition">
                  Paper & Methodology
                </a>
              </li>
              <li>
                <a href="/architecture" className="hover:text-accent transition">
                  Architecture
                </a>
              </li>
              <li>
                <a href="https://github.com/Praveen4278/camas" target="_blank" rel="noreferrer" className="hover:text-accent transition">
                  GitHub Repository
                </a>
              </li>
            </ul>
          </div>

          {/* Connect */}
          <div>
            <h4 className="font-semibold mb-4">Connect</h4>
            <div className="flex items-center space-x-4">
              <a
                href="https://www.linkedin.com/in/praveen-rajasekar-4b9b67283/"
                target="_blank"
                rel="noreferrer"
                className="text-gray-400 hover:text-accent transition text-2xl flex items-center justify-center w-10 h-10 hover:bg-gray-800 rounded-lg transition"
                title="LinkedIn"
              >
                💼
              </a>
              <a
                href="https://github.com/Praveen4278/camas"
                target="_blank"
                rel="noreferrer"
                className="text-gray-400 hover:text-accent transition text-2xl flex items-center justify-center w-10 h-10 hover:bg-gray-800 rounded-lg transition"
                title="GitHub"
              >
                🐙
              </a>
            </div>
            <p className="text-xs text-gray-600 mt-3">Follow for updates on CAMAS and AI sustainability research</p>
          </div>
        </div>

        {/* Bottom */}
        <div className="border-t border-gray-800 mt-8 pt-8 flex flex-col sm:flex-row justify-between items-center text-sm text-gray-500">
          <p>&copy; {currentYear} CAMAS. INNOVEX 2026 Submission.</p>
          <p>PS04 - Smart Cities & Sustainability</p>
        </div>
      </div>
    </footer>
  )
}
