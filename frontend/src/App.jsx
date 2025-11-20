import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Wine, BarChart3, Users, Settings } from 'lucide-react';
import Dashboard from './pages/Dashboard';
import Clientes from './pages/Clientes';
import ClienteDetalhes from './pages/ClienteDetalhes';
import './index.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-900">
        {/* Navbar */}
        <nav className="bg-slate-800 border-b border-slate-700">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <div className="flex items-center">
                <Wine className="h-8 w-8 text-wine-500" />
                <span className="ml-2 text-xl font-bold text-white">WineBrain</span>
                <span className="ml-2 text-sm text-slate-400">Sistema de Apoio à Decisão</span>
              </div>
              
              <div className="flex space-x-4">
                <Link
                  to="/"
                  className="flex items-center px-3 py-2 rounded-md text-sm font-medium text-white hover:bg-slate-700 transition"
                >
                  <BarChart3 className="h-4 w-4 mr-2" />
                  Dashboard
                </Link>
                <Link
                  to="/clientes"
                  className="flex items-center px-3 py-2 rounded-md text-sm font-medium text-white hover:bg-slate-700 transition"
                >
                  <Users className="h-4 w-4 mr-2" />
                  Clientes
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/clientes" element={<Clientes />} />
            <Route path="/clientes/:id" element={<ClienteDetalhes />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="bg-slate-800 border-t border-slate-700 mt-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <p className="text-center text-sm text-slate-400">
              © 2025 WineBrain - Sistema de Apoio à Decisão para Adega Bom Sabor
            </p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
