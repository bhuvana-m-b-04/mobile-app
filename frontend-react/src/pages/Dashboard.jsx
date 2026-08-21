import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { fetchLogs, logout } from '../services/api'
import LogCard from '../components/LogCard'

export default function Dashboard() {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()
  const username = localStorage.getItem('username') || 'User'
  const token = localStorage.getItem('token')
  const logId = parseInt(localStorage.getItem('log_id'))

  useEffect(() => { loadLogs() }, [])

  async function loadLogs() {
    setLoading(true)
    try {
      const data = await fetchLogs(token)
      setLogs(data)
    } catch (_) {}
    setLoading(false)
  }

  async function handleLogout() {
    try { await logout(token, logId) } catch (_) {}
    localStorage.clear()
    navigate('/')
  }

  const successCount = logs.filter(l => l.status === 'success').length
  const failedCount = logs.filter(l => l.status === 'failed').length

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div>
          <p style={{ fontSize: '13px', color: 'var(--muted)' }}>Welcome back</p>
          <h2>{username} 👋</h2>
        </div>
        <button className="btn-logout" onClick={handleLogout}>Logout</button>
      </div>

      <div className="stats-row">
        <div className="stat-card total">
          <div className="stat-icon">📋</div>
          <div className="stat-value">{logs.length}</div>
          <div className="stat-label">Total Sessions</div>
        </div>
        <div className="stat-card success">
          <div className="stat-icon">✅</div>
          <div className="stat-value">{successCount}</div>
          <div className="stat-label">Successful</div>
        </div>
        <div className="stat-card failed">
          <div className="stat-icon">❌</div>
          <div className="stat-value">{failedCount}</div>
          <div className="stat-label">Failed</div>
        </div>
      </div>

      <h3 className="section-title">Recent Activity</h3>

      {loading ? (
        <div className="loading">Loading activity…</div>
      ) : logs.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">🕐</div>
          <p>No login history yet</p>
        </div>
      ) : (
        <div className="logs-list">
          {logs.map(log => <LogCard key={log.id} log={log} />)}
        </div>
      )}
    </div>
  )
}
