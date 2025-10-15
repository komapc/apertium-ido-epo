import { useState } from 'react'
import { RefreshCw, CheckCircle, AlertCircle, Clock } from 'lucide-react'

type RebuildStatus = 'idle' | 'running' | 'ok' | 'error'

const RebuildButton = () => {
  const [status, setStatus] = useState<RebuildStatus>('idle')
  const [message, setMessage] = useState('')
  const [lastRebuildAt, setLastRebuildAt] = useState<string>('')

  const handleRebuild = async () => {
    if (status === 'running') return
    setStatus('running')
    setMessage('Starting rebuild process...')
    try {
      const res = await fetch('/api/admin/rebuild', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({}) })
      const data = await res.json().catch(() => ({}))
      if (!res.ok || data.error) {
        setStatus('error')
        setMessage(data.error || `Failed to trigger rebuild (${res.status})`)
        return
      }
      setStatus('ok')
      const parts: string[] = []
      if (data.status) parts.push(`Status: ${String(data.status)}`)
      if (data.message) parts.push(String(data.message))
      if (data.log) parts.push(String(data.log))
      setMessage(parts.join(' \n').trim())
      setLastRebuildAt(new Date().toISOString())
    } catch (e) {
      setStatus('error')
      setMessage('Network error while triggering rebuild')
    }
  }

  return (
    <div className="flex items-center gap-3">
      <button
        onClick={handleRebuild}
        disabled={status === 'running'}
        className="px-4 py-2 bg-red-600 hover:bg-red-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-all flex items-center gap-2"
        aria-label="Trigger rebuild"
      >
        {status === 'running' ? (
          <>
            <RefreshCw className="w-4 h-4 animate-spin" /> Rebuilding
          </>
        ) : (
          <>
            <RefreshCw className="w-4 h-4" /> Rebuild
          </>
        )}
      </button>
      {status !== 'idle' && (
        <div className={`text-sm rounded-md px-3 py-2 ${status === 'ok' ? 'bg-green-500/20 text-green-200' : status === 'error' ? 'bg-red-500/20 text-red-200' : 'bg-white/10 text-white'}`}>
          <div className="flex items-center gap-2">
            {status === 'ok' && <CheckCircle className="w-4 h-4" />}
            {status === 'error' && <AlertCircle className="w-4 h-4" />}
            <span className="whitespace-pre-wrap">{message}</span>
          </div>
          {lastRebuildAt && (
            <div className="flex items-center gap-1 mt-1 opacity-80">
              <Clock className="w-3 h-3" />
              <span>Last trigger: {lastRebuildAt}</span>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default RebuildButton


