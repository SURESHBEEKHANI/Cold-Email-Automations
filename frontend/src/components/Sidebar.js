import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Home, 
  Mail, 
  Clock, 
  Settings, 
  BarChart3, 
  Users, 
  FileText,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';

const Sidebar = ({ isCollapsed, setIsCollapsed }) => {
  const location = useLocation();

  const navItems = [
    { 
      path: '/', 
      label: 'Dashboard', 
      icon: Home,
      description: 'Overview and analytics'
    },
    { 
      path: '/generate', 
      label: 'Generate Emails', 
      icon: Mail,
      description: 'Create cold emails'
    },
    { 
      path: '/history', 
      label: 'History', 
      icon: Clock,
      description: 'View past emails'
    },
    { 
      path: '/templates', 
      label: 'Templates', 
      icon: FileText,
      description: 'Email templates'
    },
    { 
      path: '/analytics', 
      label: 'Analytics', 
      icon: BarChart3,
      description: 'Performance metrics'
    },
    { 
      path: '/contacts', 
      label: 'Contacts', 
      icon: Users,
      description: 'Manage contacts'
    },
    { 
      path: '/settings', 
      label: 'Settings', 
      icon: Settings,
      description: 'App configuration'
    },
  ];

  return (
    <div className={`bg-white border-r border-gray-200 transition-all duration-300 ease-in-out ${
      isCollapsed ? 'w-16' : 'w-64'
    }`}>
      {/* Sidebar Header */}
      <div className="flex items-center justify-between h-16 px-4 border-b border-gray-200">
        {!isCollapsed && (
          <div className="flex items-center space-x-2">
            <div className="inline-flex items-center justify-center h-8 w-8 rounded-lg bg-primary-600 text-white text-sm font-bold">
              <Mail className="h-4 w-4" />
            </div>
            <span className="text-lg font-semibold text-gray-900">Cold Email</span>
          </div>
        )}
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="p-1 rounded-lg hover:bg-gray-100 transition-colors duration-200"
        >
          {isCollapsed ? (
            <ChevronRight className="h-4 w-4 text-gray-600" />
          ) : (
            <ChevronLeft className="h-4 w-4 text-gray-600" />
          )}
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`group flex items-center px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                isActive
                  ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                  : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
              }`}
            >
              <Icon className={`h-5 w-5 ${
                isActive ? 'text-primary-600' : 'text-gray-400 group-hover:text-gray-600'
              }`} />
              {!isCollapsed && (
                <span className="ml-3">{item.label}</span>
              )}
              {isCollapsed && (
                <div className="absolute left-full ml-2 px-2 py-1 bg-gray-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap z-50">
                  {item.label}
                </div>
              )}
            </Link>
          );
        })}
      </nav>

      {/* Sidebar Footer */}
      {!isCollapsed && (
        <div className="p-4 border-t border-gray-200">
          <div className="bg-gray-50 rounded-lg p-3">
            <div className="flex items-center space-x-3">
              <div className="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center">
                <span className="text-sm font-medium text-primary-700">U</span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">User</p>
                <p className="text-xs text-gray-500 truncate">user@example.com</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Sidebar; 