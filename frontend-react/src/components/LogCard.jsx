export default function LogCard({ log }) {
  const isSuccess = log.status === 'success'
  const isActive = !log.logout_time && log.status === 'success'

  // Append 'Z' so JS treats the naive UTC string from the backend as UTC, not local
  const asUTC = (iso) => (iso && !iso.endsWith('Z') && !iso.includes('+') ? iso + 'Z' : iso)

  const fmt = (iso) =>
    new Date(asUTC(iso)).toLocaleString(undefined, {
      month: 'short', day: '2-digit', year: 'numeric',
      hour: '2-digit', minute: '2-digit', hour12: true,
    })

  const duration = () => {
    if (!log.logout_time) return null
    const ms = new Date(asUTC(log.logout_time)) - new Date(asUTC(log.login_time))
    const s = Math.floor(ms / 1000)
    const m = Math.floor(s / 60)
    const h = Math.floor(m / 60)
    if (h > 0) return `${h}h ${m % 60}m`
    if (m > 0) return `${m}m ${s % 60}s`
    return `${s}s`
  }

  return (
    <div className="log-card">
      <div className="log-card-header">
        <span className={`badge ${isSuccess ? 'success' : 'failed'}`}>
          {isSuccess ? '✓ Success' : '✗ Failed'}
        </span>
        {isActive && <span className="badge active">● Active</span>}
      </div>
      <div className="log-info">
        <div className="info-row">
          <span className="info-label">Login</span>
          <span className="info-value">{fmt(log.login_time)}</span>
        </div>
        {log.logout_time && (
          <>
            <div className="info-row">
              <span className="info-label">Logout</span>
              <span className="info-value">{fmt(log.logout_time)}</span>
            </div>
            <div className="info-row">
              <span className="info-label">Duration</span>
              <span className="info-value">{duration()}</span>
            </div>
          </>
        )}
        {log.ip_address && (
          <div className="info-row">
            <span className="info-label">IP</span>
            <span className="info-value">{log.ip_address}</span>
          </div>
        )}
        {log.device_info && (
          <div className="info-row">
            <span className="info-label">Device</span>
            <span className="info-value">
              {log.device_info.length > 80 ? log.device_info.slice(0, 80) + '…' : log.device_info}
            </span>
          </div>
        )}
      </div>
    </div>
  )
}
