import { useState } from 'react'
import { Loader2, Copy, CheckCircle } from 'lucide-react'

interface TextTranslatorProps {
  direction: 'ido-epo' | 'epo-ido'
}

const TextTranslator = ({ direction }: TextTranslatorProps) => {
  const [inputText, setInputText] = useState('')
  const [outputText, setOutputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [copied, setCopied] = useState(false)

  const handleTranslate = async () => {
    if (!inputText.trim()) return

    setIsLoading(true)
    try {
      const response = await fetch('/api/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: inputText,
          direction: direction,
        }),
      })

      const data = await response.json()
      setOutputText(data.translation || 'Translation failed')
    } catch (error) {
      console.error('Translation error:', error)
      setOutputText('Error: Could not connect to translation service')
    } finally {
      setIsLoading(false)
    }
  }

  const handleCopy = async () => {
    await navigator.clipboard.writeText(outputText)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="grid md:grid-cols-2 gap-6">
      {/* Input Panel */}
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 shadow-xl">
        <h2 className="text-xl font-semibold text-white mb-4">
          {direction === 'ido-epo' ? 'Ido' : 'Esperanto'} Input
        </h2>
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder={`Enter ${direction === 'ido-epo' ? 'Ido' : 'Esperanto'} text here...`}
          className="w-full h-64 p-4 bg-white/5 border border-white/20 rounded-lg text-white placeholder-purple-300/50 focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none"
          aria-label="Input text to translate"
        />
        <button
          onClick={handleTranslate}
          disabled={isLoading || !inputText.trim()}
          className="mt-4 w-full py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-all flex items-center justify-center gap-2"
          aria-label="Translate text"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Translating...
            </>
          ) : (
            'Translate'
          )}
        </button>
      </div>

      {/* Output Panel */}
      <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 shadow-xl">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-white">
            {direction === 'ido-epo' ? 'Esperanto' : 'Ido'} Translation
          </h2>
          {outputText && (
            <button
              onClick={handleCopy}
              className="p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all"
              aria-label="Copy translation to clipboard"
            >
              {copied ? (
                <CheckCircle className="w-5 h-5 text-green-400" />
              ) : (
                <Copy className="w-5 h-5 text-white" />
              )}
            </button>
          )}
        </div>
        <div className="w-full h-64 p-4 bg-white/5 border border-white/20 rounded-lg text-white overflow-y-auto">
          {outputText || (
            <span className="text-purple-300/50">Translation will appear here...</span>
          )}
        </div>
      </div>
    </div>
  )
}

export default TextTranslator

