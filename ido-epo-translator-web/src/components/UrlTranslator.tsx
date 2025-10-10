import { useState } from 'react'
import { Loader2, ExternalLink } from 'lucide-react'

interface UrlTranslatorProps {
  direction: 'ido-epo' | 'epo-ido'
}

const UrlTranslator = ({ direction }: UrlTranslatorProps) => {
  const [url, setUrl] = useState('')
  const [originalText, setOriginalText] = useState('')
  const [translatedText, setTranslatedText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handleTranslate = async () => {
    if (!url.trim()) return

    setIsLoading(true)
    setError('')
    setOriginalText('')
    setTranslatedText('')

    try {
      const response = await fetch('/api/translate-url', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: url,
          direction: direction,
        }),
      })

      const data = await response.json()
      
      if (data.error) {
        setError(data.error)
      } else {
        setOriginalText(data.original || '')
        setTranslatedText(data.translation || '')
      }
    } catch (err) {
      console.error('Translation error:', err)
      setError('Error: Could not connect to translation service')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* URL Input */}
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 shadow-xl">
        <h2 className="text-xl font-semibold text-white mb-4">Enter URL</h2>
        <div className="flex gap-3">
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://io.wikipedia.org/wiki/..."
            className="flex-1 p-4 bg-white/5 border border-white/20 rounded-lg text-white placeholder-purple-300/50 focus:outline-none focus:ring-2 focus:ring-purple-500"
            aria-label="Enter URL to translate"
          />
          <button
            onClick={handleTranslate}
            disabled={isLoading || !url.trim()}
            className="px-8 py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-all flex items-center gap-2"
            aria-label="Translate URL"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Loading...
              </>
            ) : (
              'Translate'
            )}
          </button>
        </div>
        {error && (
          <div className="mt-4 p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-200">
            {error}
          </div>
        )}
      </div>

      {/* Side-by-Side Comparison */}
      {(originalText || translatedText) && (
        <div className="grid md:grid-cols-2 gap-6">
          {/* Original Text */}
          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-white">
                Original ({direction === 'ido-epo' ? 'Ido' : 'Esperanto'})
              </h2>
              <a
                href={url}
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all"
                aria-label="Open original URL"
              >
                <ExternalLink className="w-5 h-5 text-white" />
              </a>
            </div>
            <div className="p-4 bg-white/5 border border-white/20 rounded-lg max-h-96 overflow-y-auto">
              <p className="text-white whitespace-pre-wrap">{originalText}</p>
            </div>
          </div>

          {/* Translated Text */}
          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 shadow-xl">
            <h2 className="text-xl font-semibold text-white mb-4">
              Translation ({direction === 'ido-epo' ? 'Esperanto' : 'Ido'})
            </h2>
            <div className="p-4 bg-white/5 border border-white/20 rounded-lg max-h-96 overflow-y-auto">
              <p className="text-white whitespace-pre-wrap">{translatedText}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default UrlTranslator

