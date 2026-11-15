import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'

import LandingPage from './pages/LandingPage'
import OrchestrationStudio from './pages/OrchestrationStudio'
import Dashboard from './pages/Dashboard'
import ArchitecturePage from './pages/ArchitecturePage'
import BenchmarksPage from './pages/BenchmarksPage'
import ResearchPage from './pages/ResearchPage'
import ResultsPage from './pages/ResultsPage'

import NavBar from './components/NavBar'
import Footer from './components/Footer'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-950 text-white flex flex-col">
        <NavBar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/studio" element={<OrchestrationStudio />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/architecture" element={<ArchitecturePage />} />
            <Route path="/benchmarks" element={<BenchmarksPage />} />
            <Route path="/research" element={<ResearchPage />} />
            <Route path="/results" element={<ResultsPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  )
}

export default App
