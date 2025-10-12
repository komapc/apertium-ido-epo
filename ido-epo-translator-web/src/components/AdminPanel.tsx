import { useState } from 'react'
import { RefreshCw, AlertCircle, CheckCircle, Terminal } from 'lucide-react'

const AdminPanel = () => {
  const [isRebuilding, setIsRebuilding] = useState(false)
  const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle')
  const [logs, setLogs] = useState<string[]>([])
  const [password, setPassword] = useState('')

  const handleRebuild = async () => {
    if (!password) {
      setStatus('error')
      setLogs(['Error: Admin password required'])
      return
    }

    setIsRebuilding(true)
    setStatus('idle')
    setLogs(['Starting rebuild process...'])

    try {
      const response = await fetch('/api/admin/rebuild', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password }),
      })

      const data = await response.json()

      if (data.error) {
        setStatus('error')
        setLogs((prev) => [...prev, `Error: ${data.error}`])
      } else {
        setStatus('success')
        setLogs((prev) => [...prev, ...data.logs])
      }
    } catch (error) {
      setStatus('error')
      setLogs((prev) => [...prev, 'Error: Could not connect to admin service'])
    } finally {
      setIsRebuilding(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Warning Banner */}
      <div className="bg-red-500/20 border border-red-500/50 rounded-xl p-4 flex items-start gap-3">
        <AlertCircle className="w-6 h-6 text-red-400 flex-shrink-0 mt-1" />
        <div className="text-red-200">
          <h3 className="font-semibold mb-1">Admin Panel - Restricted Access</h3>
          <p className="text-sm">
            This panel allows you to rebuild and redeploy the Apertium translation engine. 
            This operation will pull the latest code from the repositories and recompile 
            all dictionaries.
          </p>
        </div>
      </div>

      {/* Rebuild Control */}
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 shadow-xl">
        <h2 className="text-2xl font-semibold text-white mb-4 flex items-center gap-2">
          <RefreshCw className="w-6 h-6" />
          Rebuild Translation Engine
        </h2>

        <div className="space-y-4">
          <div>
            <label htmlFor="password" className="block text-white font-medium mb-2">
              Admin Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter admin password"
              className="w-full p-3 bg-white/5 border border-white/20 rounded-lg text-white placeholder-purple-300/50 focus:outline-none focus:ring-2 focus:ring-purple-500"
              aria-label="Admin password"
            />
          </div>

          <button
            onClick={handleRebuild}
            disabled={isRebuilding || !password}
            className="w-full py-3 bg-red-600 hover:bg-red-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-all flex items-center justify-center gap-2"
            aria-label="Start rebuild process"
          >
            {isRebuilding ? (
              <>
                <RefreshCw className="w-5 h-5 animate-spin" />
                Rebuilding...
              </>
            ) : (
              <>
                <RefreshCw className="w-5 h-5" />
                Rebuild & Deploy
              </>
            )}
          </button>
        </div>

        {/* Status Indicator */}
        {status !== 'idle' && (
          <div className={`mt-4 p-4 rounded-lg flex items-center gap-3 ${
            status === 'success' 
              ? 'bg-green-500/20 border border-green-500/50' 
              : 'bg-red-500/20 border border-red-500/50'
          }`}>
            {status === 'success' ? (
              <>
                <CheckCircle className="w-6 h-6 text-green-400" />
                <span className="text-green-200 font-medium">
                  Rebuild completed successfully!
                </span>
              </>
            ) : (
              <>
                <AlertCircle className="w-6 h-6 text-red-400" />
                <span className="text-red-200 font-medium">
                  Rebuild failed. Check logs below.
                </span>
              </>
            )}
          </div>
        )}
      </div>

      {/* Build Logs */}
      {logs.length > 0 && (
        <div className="bg-black/50 backdrop-blur-sm rounded-xl p-6 shadow-xl">
          <h3 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
            <Terminal className="w-5 h-5" />
            Build Logs
          </h3>
          <div className="bg-black/50 rounded-lg p-4 font-mono text-sm text-green-400 max-h-96 overflow-y-auto">
            {logs.map((log, index) => (
              <div key={index} className="mb-1">
                {log}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Instructions */}
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 shadow-xl">
        <h3 className="text-xl font-semibold text-white mb-3">Instructions</h3>
        <div className="text-purple-200 space-y-2 text-sm">
          <p>1. Enter the admin password (set in environment variables)</p>
          <p>2. Click "Rebuild & Deploy" to start the process</p>
          <p>3. The system will:</p>
          <ul className="list-disc list-inside ml-4 space-y-1">
            <li>Pull latest code from apertium-ido repository</li>
            <li>Pull latest code from apertium-ido-epo repository</li>
            <li>Recompile all dictionaries and transfer rules</li>
            <li>Restart the translation service</li>
          </ul>
          <p className="pt-2 text-yellow-300">
            ⚠️ The translation service will be briefly unavailable during rebuild (~2-5 minutes)
          </p>
        </div>
      </div>
    </div>
  )
}

export default AdminPanel

