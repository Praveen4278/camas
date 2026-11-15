import { Link } from 'react-router-dom'
import { useState } from 'react'

export default function NavBar() {
  const [isOpen, setIsOpen] = useState(false)

  const links = [
    { path: '/', label: 'Home' },
    { path: '/studio', label: 'Orchestration' },
    { path: '/dashboard', label: 'Dashboard' },
    { path: '/architecture', label: 'Architecture' },
    { path: '/benchmarks', label: 'Benchmarks' },
    { path: '/research', label: 'Research' },
    { path: '/results', label: 'Results' },
  ]

  return (
    <nav className="sticky top-0 z-50 bg-gray-950 border-b border-gray-800 backdrop-blur">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 group">
            <div className="w-8 h-8 bg-accent rounded-lg flex items-center justify-center font-bold text-darker text-sm">
              C
            </div>
            <span className="font-bold text-lg hidden sm:inline group-hover:text-accent transition">
              CAMAS
            </span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-1">
            {links.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className="px-3 py-2 text-sm font-medium text-gray-300 hover:text-accent hover:bg-gray-900 rounded-lg transition"
              >
                {link.label}
              </Link>
            ))}
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden text-gray-300 hover:text-accent"
            onClick={() => setIsOpen(!isOpen)}
          >
            {isOpen ? '✕' : '☰'}
          </button>
        </div>

        {/* Mobile Menu */}
        {isOpen && (
          <div className="md:hidden border-t border-gray-800">
            <div className="px-2 pt-2 pb-3 space-y-1">
              {links.map((link) => (
                <Link
                  key={link.path}
                  to={link.path}
                  className="block px-3 py-2 text-sm font-medium text-gray-300 hover:text-accent hover:bg-gray-900 rounded-lg transition"
                  onClick={() => setIsOpen(false)}
                >
                  {link.label}
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
