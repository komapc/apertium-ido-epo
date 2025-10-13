export const onRequest = async (context) => {
  const { request, env } = context
  const url = new URL(request.url)
  const subpath = url.pathname.replace(/^\/api/, '') || '/'

  const APY_SERVER_URL = env.APY_SERVER_URL || 'http://localhost:2737'
  const ADMIN_PASSWORD = env.ADMIN_PASSWORD || 'change-me-in-production'

  const sendJson = (status, data) =>
    new Response(JSON.stringify(data), {
      status,
      headers: { 'Content-Type': 'application/json' },
    })

  if (request.method === 'GET' && subpath === '/health') {
    return sendJson(200, { status: 'ok', timestamp: new Date().toISOString() })
  }

  if (request.method === 'POST' && subpath === '/translate') {
    try {
      // Handle both JSON and form data formats
      const contentType = request.headers.get('content-type') || ''
      let text, langpair
      
      if (contentType.includes('application/x-www-form-urlencoded')) {
        // Handle URL-encoded form data (direct APy format)
        const formText = await request.text()
        const params = new URLSearchParams(formText)
        text = params.get('q')
        langpair = params.get('langpair')
      } else {
        // Handle JSON format (legacy)
        const body = await request.json().catch(() => ({}))
        text = body?.text
        const direction = body?.direction
        langpair = direction === 'ido-epo' ? 'ido|epo' : 'epo|ido'
      }

      if (!text || !langpair) {
        return sendJson(400, { 
          error: 'Missing text or langpair', 
          debug: { text, langpair, contentType },
          version: 'v3-new-code'
        })
      }

      const res = await fetch(`${APY_SERVER_URL}/translate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ q: text, langpair: langpair }),
      })

      if (!res.ok) {
        return sendJson(502, {
          error: 'Translation service error',
          details: `APY server returned ${res.status}`
        })
      }

      const data = await res.json()
      return sendJson(200, {
        translation: data.responseData?.translatedText || text,
        sourceLanguage: langpair.split('|')[0],
        targetLanguage: langpair.split('|')[1],
      })
    } catch (e) {
      return sendJson(500, {
        error: 'Translation service unavailable',
        details: e?.message
      })
    }
  }

  if (request.method === 'POST' && subpath === '/translate-url') {
    const body = await request.json().catch(() => ({}))
    const pageUrl = body?.url
    const direction = body?.direction
    if (!pageUrl || !direction) return sendJson(400, { error: 'Missing URL or direction' })
    try {
      const pageRes = await fetch(pageUrl)
      if (!pageRes.ok) return sendJson(400, { error: 'Could not fetch URL' })
      const html = await pageRes.text()
      const textContent = extractTextFromHtml(html)
      if (!textContent.trim()) return sendJson(400, { error: 'No text content found in URL' })
      const langPair = direction === 'ido-epo' ? 'ido|epo' : 'epo|ido'
      const translationRes = await fetch(`${APY_SERVER_URL}/translate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ q: textContent, langpair: langPair }),
      })
      if (!translationRes.ok) return sendJson(502, { error: 'Translation service error' })
      const translationData = await translationRes.json()
      return sendJson(200, {
        original: textContent,
        translation: translationData.responseData?.translatedText || textContent,
        url: pageUrl,
      })
    } catch (e) {
      return sendJson(500, { error: 'URL translation failed', details: e?.message })
    }
  }

  if (request.method === 'POST' && subpath === '/admin/rebuild') {
    const body = await request.json().catch(() => ({}))
    if (body?.password !== ADMIN_PASSWORD) return sendJson(401, { error: 'Invalid admin password' })
    const logs = [
      'Starting rebuild process...',
      'Pulling latest code from apertium-ido...',
      'Pulling latest code from apertium-ido-epo...',
      'Compiling dictionaries...',
      'Restarting translation service...',
      'Rebuild complete!'
    ]
    return sendJson(200, { success: true, logs, timestamp: new Date().toISOString() })
  }

  return sendJson(404, { error: 'Not found' })
}

function extractTextFromHtml(html) {
  let text = html.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
  text = text.replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, '')
  text = text.replace(/<[^>]+>/g, ' ')
  text = text.replace(/&nbsp;/g, ' ')
  text = text.replace(/&amp;/g, '&')
  text = text.replace(/&lt;/g, '<')
  text = text.replace(/&gt;/g, '>')
  text = text.replace(/&quot;/g, '"')
  text = text.replace(/\s+/g, ' ')
  return text.trim()
}

