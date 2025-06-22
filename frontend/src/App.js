import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import EmailGenerator from './pages/EmailGenerator';
import History from './pages/History';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/generate" element={<EmailGenerator />} />
          <Route path="/history" element={<History />} />
          {/* Add more routes for new pages */}
          <Route path="/templates" element={<div className="text-center py-12"><h2 className="text-2xl font-bold text-gray-900">Templates</h2><p className="text-gray-600 mt-2">Email templates page coming soon...</p></div>} />
          <Route path="/analytics" element={<div className="text-center py-12"><h2 className="text-2xl font-bold text-gray-900">Analytics</h2><p className="text-gray-600 mt-2">Analytics dashboard coming soon...</p></div>} />
          <Route path="/contacts" element={<div className="text-center py-12"><h2 className="text-2xl font-bold text-gray-900">Contacts</h2><p className="text-gray-600 mt-2">Contact management coming soon...</p></div>} />
          <Route path="/settings" element={<div className="text-center py-12"><h2 className="text-2xl font-bold text-gray-900">Settings</h2><p className="text-gray-600 mt-2">Settings page coming soon...</p></div>} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App; 