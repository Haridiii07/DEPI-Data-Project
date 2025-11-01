import React, { useState } from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Users, TrendingUp, Calendar, BookOpen, ChevronRight, AlertCircle, CheckCircle } from 'lucide-react';

const EducationalDashboard = () => {
  const [currentView, setCurrentView] = useState('overview');
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [filters, setFilters] = useState({
    cohort: 'All',
    subject: 'All',
    timeRange: '6months'
  });

  // Sample data
  const kpiData = {
    attendanceRate: 94.2,
    averageScore: 78.5,
    totalStudents: 342,
    atRiskStudents: 23
  };

  const trendData = [
    { month: 'Jan', Math: 75, Science: 78, English: 82 },
    { month: 'Feb', Math: 77, Science: 80, English: 81 },
    { month: 'Mar', Math: 76, Science: 79, English: 83 },
    { month: 'Apr', Math: 73, Science: 77, English: 80 },
    { month: 'May', Math: 72, Science: 76, English: 79 },
    { month: 'Jun', Math: 71, Science: 75, English: 78 }
  ];

  const studentList = [
    { id: 1, name: 'Sarah Johnson', score: 85, attendance: 96, status: 'good' },
    { id: 2, name: 'Michael Chen', score: 72, attendance: 88, status: 'warning' },
    { id: 3, name: 'Emma Davis', score: 91, attendance: 98, status: 'good' },
    { id: 4, name: 'James Wilson', score: 68, attendance: 82, status: 'at-risk' },
    { id: 5, name: 'Olivia Brown', score: 88, attendance: 94, status: 'good' }
  ];

  const studentDetailData = {
    name: 'Michael Chen',
    grade: '10th Grade',
    cohort: '2024',
    gradeHistory: [
      { assignment: 'Quiz 1', score: 85, date: '2024-01-15' },
      { assignment: 'Midterm', score: 78, date: '2024-02-20' },
      { assignment: 'Project', score: 65, date: '2024-03-10' },
      { assignment: 'Quiz 2', score: 70, date: '2024-04-05' },
      { assignment: 'Final', score: 72, date: '2024-05-15' }
    ],
    attendance: [
      { month: 'Jan', rate: 95 },
      { month: 'Feb', rate: 90 },
      { month: 'Mar', rate: 85 },
      { month: 'Apr', rate: 88 },
      { month: 'May', rate: 82 }
    ],
    missingAssignments: 3,
    notes: 'Student showing declining performance in recent assessments. Missing key homework assignments.'
  };

  const cohortComparison = [
    { cohort: '2022', avgScore: 82, students: 120 },
    { cohort: '2023', avgScore: 79, students: 115 },
    { cohort: '2024', avgScore: 76, students: 107 }
  ];

  const KPICard = ({ title, value }) => (
    <div className="bg-white border-2 border-gray-800 p-6 text-center">
      <p className="text-6xl font-bold text-gray-900 mb-2">{value}</p>
      <p className="text-xs uppercase tracking-wide text-gray-700 font-semibold">{title}</p>
    </div>
  );

  const OverviewScreen = () => (
    <div>
      <div className="bg-white border-2 border-gray-800 p-4 mb-6">
        <h2 className="text-xl font-bold text-center mb-6 uppercase tracking-wide">Performance Dashboard</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <KPICard title="Overall Attendance Rate" value="85%" />
          <KPICard title="Avg. Score" value="72" />
          <KPICard title="Pass Rate" value="90%" />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-gray-50 border-2 border-gray-800 p-4">
          <h3 className="text-sm font-bold uppercase mb-3">Filter Panel</h3>
          <div className="space-y-2 text-sm">
            <p><span className="font-semibold">Cohort:</span> All</p>
            <p><span className="font-semibold">Subject:</span> Math</p>
            <p><span className="font-semibold">Subject:</span> Math</p>
            <p><span className="font-semibold">Time:</span> Last Month</p>
          </div>
        </div>

        <div className="bg-white border-2 border-gray-800 p-4">
          <h3 className="text-sm font-bold uppercase mb-3 text-center">Grade History Timeline</h3>
          <ResponsiveContainer width="100%" height={180}>
            <LineChart data={trendData.slice(0, 5)}>
              <CartesianGrid strokeDasharray="3 3" stroke="#d1d5db" />
              <XAxis dataKey="month" stroke="#374151" tick={{ fontSize: 11 }} />
              <YAxis stroke="#374151" tick={{ fontSize: 11 }} domain={[60, 100]} />
              <Line type="monotone" dataKey="Math" stroke="#374151" strokeWidth={2} dot={{ fill: '#374151', r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="bg-white border-2 border-gray-800 p-4">
        <h3 className="text-sm font-bold uppercase mb-3 text-center">Main Trend Chart</h3>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={trendData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#d1d5db" />
            <XAxis dataKey="month" stroke="#374151" tick={{ fontSize: 11 }} />
            <YAxis stroke="#374151" tick={{ fontSize: 11 }} />
            <Line type="monotone" dataKey="Math" stroke="#374151" strokeWidth={2} dot={{ fill: '#374151', r: 3 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );

  const StudentProfileScreen = () => (
    <div>
      <button 
        onClick={() => setCurrentView('overview')}
        className="mb-4 text-gray-900 hover:text-gray-700 font-bold text-sm flex items-center gap-1 uppercase"
      >
        ← Back to Overview
      </button>

      <div className="bg-white border-2 border-gray-800 p-6 mb-6">
        <h2 className="text-xl font-bold text-center mb-6 uppercase">Student Profile: Jane Doe</h2>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <div className="bg-gray-50 border-2 border-gray-800 p-4">
            <h3 className="text-sm font-bold uppercase mb-3">Filter Panel</h3>
            <div className="space-y-2 text-sm mb-4">
              <p><span className="font-semibold">Cohort:</span></p>
              <p className="ml-2">Select Cohort A</p>
              <div className="border border-gray-400 p-2 text-xs bg-white">
                Math/Math
              </div>
            </div>
            
            <h3 className="text-sm font-bold uppercase mb-3 mt-4">Performance Summary</h3>
            <ResponsiveContainer width="100%" height={120}>
              <BarChart data={[
                { week: 'W1', score: 75 },
                { week: 'W2', score: 82 },
                { week: 'W3', score: 88 },
                { week: 'W4', score: 95 }
              ]}>
                <CartesianGrid strokeDasharray="3 3" stroke="#d1d5db" />
                <XAxis dataKey="week" stroke="#374151" tick={{ fontSize: 10 }} />
                <YAxis stroke="#374151" tick={{ fontSize: 10 }} />
                <Bar dataKey="score" fill="#6b7280" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div>
            <div className="bg-gray-50 border-2 border-gray-800 p-4 mb-4">
              <h3 className="text-sm font-bold uppercase mb-3 text-center">Attendance Log</h3>
              <div className="grid grid-cols-7 gap-1">
                {['M', 'T', 'W', 'T', 'F', 'S', 'S'].map((day, i) => (
                  <div key={i} className="text-center text-xs font-bold p-1">{day}</div>
                ))}
                {Array.from({ length: 21 }).map((_, i) => (
                  <div 
                    key={i} 
                    className={`aspect-square border border-gray-400 flex items-center justify-center text-xs ${
                      i === 6 || i === 13 ? 'bg-gray-400' : 'bg-white'
                    }`}
                  >
                    {i === 6 || i === 13 ? '✓' : ''}
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-gray-50 border-2 border-gray-800 p-4">
              <h3 className="text-sm font-bold uppercase mb-2">Performance Log</h3>
              <ul className="text-xs space-y-1">
                <li>• Oct 26: Present</li>
                <li>• Oct 27: Present</li>
                <li>• Oct 28: Absent</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="bg-white border-2 border-gray-800 p-4 mb-6">
          <h3 className="text-sm font-bold uppercase mb-3 text-center">Comparative Trend Chart</h3>
          <p className="text-xs text-right mb-2 uppercase font-semibold">Cohort A</p>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart>
              <CartesianGrid strokeDasharray="3 3" stroke="#d1d5db" />
              <XAxis stroke="#374151" tick={{ fontSize: 10 }} />
              <YAxis stroke="#374151" tick={{ fontSize: 10 }} />
              <Line 
                data={[
                  { x: 1, y: 60 }, { x: 2, y: 75 }, { x: 3, y: 70 }, { x: 4, y: 85 }, { x: 5, y: 80 }, { x: 6, y: 90 }
                ]} 
                type="monotone" 
                dataKey="y" 
                stroke="#374151" 
                strokeWidth={2} 
                dot={{ fill: '#374151', r: 4 }}
                strokeDasharray="5 5"
              />
              <Line 
                data={[
                  { x: 1, y: 70 }, { x: 2, y: 65 }, { x: 3, y: 78 }, { x: 4, y: 60 }, { x: 5, y: 75 }, { x: 6, y: 70 }
                ]} 
                type="monotone" 
                dataKey="y" 
                stroke="#374151" 
                strokeWidth={2} 
                dot={{ fill: 'white', stroke: '#374151', strokeWidth: 2, r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
          <p className="text-xs text-right mt-2 uppercase font-semibold">Cohort B</p>
        </div>

        <div className="bg-white border-2 border-gray-800 p-4">
          <h3 className="text-sm font-bold uppercase mb-3 text-center">Subject Performance Heatmap</h3>
          <div className="space-y-2">
            {[
              { subject: 'MATH', cells: [0, 0, 0, 3, 0, 0, 0, 3, 0] },
              { subject: 'MATT', cells: [0, 0, 0, 0, 0, 0, 0, 0, 0] },
              { subject: 'SCIENCE', cells: [0, 0, 0, 0, 0, 0, 3, 0, 0] },
              { subject: 'HISTORY', cells: [0, 3, 0, 0, 0, 0, 0, 0, 0] },
              { subject: 'HISTORY', cells: [0, 0, 0, 0, 0, 0, 0, 3, 0] },
              { subject: 'Q1', cells: [0, 0, 0, 0, 0, 0, 0, 3, 0] }
            ].map((row, i) => (
              <div key={i} className="grid grid-cols-10 gap-1 items-center">
                <div className="text-xs font-semibold pr-2 text-right">{row.subject}</div>
                {row.cells.map((cell, j) => (
                  <div 
                    key={j} 
                    className={`aspect-square border border-gray-400 ${
                      cell === 3 ? 'bg-gray-600' : 'bg-white'
                    }`}
                  />
                ))}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const CohortAnalysisScreen = () => (
    <div>
      <button 
        onClick={() => setCurrentView('overview')}
        className="mb-4 text-gray-900 hover:text-gray-700 font-bold text-sm flex items-center gap-1 uppercase"
      >
        ← Back to Overview
      </button>

      <div className="bg-white border-2 border-gray-800 p-6">
        <h2 className="text-xl font-bold text-center mb-6 uppercase">Cohort Analysis</h2>

        <div className="bg-white border-2 border-gray-800 p-4 mb-6">
          <h3 className="text-sm font-bold uppercase mb-3 text-center">Comparative Trend Chart</h3>
          <p className="text-xs text-right mb-2 uppercase font-semibold">Cohort A</p>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart>
              <CartesianGrid strokeDasharray="3 3" stroke="#d1d5db" />
              <XAxis stroke="#374151" tick={{ fontSize: 10 }} />
              <YAxis stroke="#374151" tick={{ fontSize: 10 }} />
              <Line 
                data={[
                  { x: 1, y: 60 }, { x: 2, y: 75 }, { x: 3, y: 70 }, { x: 4, y: 85 }, { x: 5, y: 80 }, { x: 6, y: 90 }
                ]} 
                type="monotone" 
                dataKey="y" 
                stroke="#374151" 
                strokeWidth={2} 
                dot={{ fill: '#374151', r: 4 }}
                strokeDasharray="5 5"
              />
              <Line 
                data={[
                  { x: 1, y: 70 }, { x: 2, y: 65 }, { x: 3, y: 78 }, { x: 4, y: 60 }, { x: 5, y: 75 }, { x: 6, y: 70 }
                ]} 
                type="monotone" 
                dataKey="y" 
                stroke="#374151" 
                strokeWidth={2} 
                dot={{ fill: 'white', stroke: '#374151', strokeWidth: 2, r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
          <p className="text-xs text-right mt-2 uppercase font-semibold">Cohort B</p>
        </div>

        <div className="bg-white border-2 border-gray-800 p-4">
          <h3 className="text-sm font-bold uppercase mb-3 text-center">Subject Performance Heatmap</h3>
          <div className="space-y-2">
            {[
              { subject: 'MATH', cells: [0, 0, 0, 3, 0, 0, 0, 3, 0] },
              { subject: 'MATT', cells: [0, 0, 0, 0, 0, 0, 0, 0, 0] },
              { subject: 'SCIENCE', cells: [0, 0, 0, 0, 0, 0, 3, 0, 0] },
              { subject: 'HISTORY', cells: [0, 3, 0, 0, 0, 0, 0, 0, 0] },
              { subject: 'HISTORY', cells: [0, 0, 0, 0, 0, 0, 0, 3, 0] },
              { subject: 'Q1', cells: [0, 0, 0, 0, 0, 0, 0, 3, 0] }
            ].map((row, i) => (
              <div key={i} className="grid grid-cols-10 gap-1 items-center">
                <div className="text-xs font-semibold pr-2 text-right">{row.subject}</div>
                {row.cells.map((cell, j) => (
                  <div 
                    key={j} 
                    className={`aspect-square border border-gray-400 ${
                      cell === 3 ? 'bg-gray-600' : 'bg-white'
                    }`}
                  />
                ))}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-stone-200">
      {/* Header */}
      <header className="bg-white border-b-4 border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <BookOpen className="w-8 h-8 text-gray-800" />
              <h1 className="text-2xl font-bold text-gray-900 uppercase tracking-wide">EduAnalytics Dashboard</h1>
            </div>
            <nav className="flex gap-4">
              <button 
                onClick={() => setCurrentView('overview')}
                className={`px-4 py-2 font-bold uppercase text-sm transition border-2 ${
                  currentView === 'overview' 
                    ? 'bg-gray-800 text-white border-gray-800' 
                    : 'text-gray-800 border-gray-800 bg-white hover:bg-gray-100'
                }`}
              >
                1. Overview Screen
              </button>
              <button 
                onClick={() => setCurrentView('student')}
                className={`px-4 py-2 font-bold uppercase text-sm transition border-2 ${
                  currentView === 'student' 
                    ? 'bg-gray-800 text-white border-gray-800' 
                    : 'text-gray-800 border-gray-800 bg-white hover:bg-gray-100'
                }`}
              >
                2. Student Profile
              </button>
              <button 
                onClick={() => setCurrentView('cohort')}
                className={`px-4 py-2 font-bold uppercase text-sm transition border-2 ${
                  currentView === 'cohort' 
                    ? 'bg-gray-800 text-white border-gray-800' 
                    : 'text-gray-800 border-gray-800 bg-white hover:bg-gray-100'
                }`}
              >
                3. Cohort Analysis
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {currentView === 'overview' && <OverviewScreen />}
        {currentView === 'student' && <StudentProfileScreen />}
        {currentView === 'cohort' && <CohortAnalysisScreen />}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t-4 border-gray-800 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <p className="text-sm text-gray-700 text-center font-semibold uppercase tracking-wide">
            Wireframe-Based Design • High Contrast • Accessible
          </p>
        </div>
      </footer>
    </div>
  );
};

export default EducationalDashboard;