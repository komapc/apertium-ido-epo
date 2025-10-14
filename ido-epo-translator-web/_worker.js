// Cloudflare Pages _worker.js for Ido-Esperanto Translator
// Handles API routes and serves static assets from Pages ASSETS binding

export default {
  async fetch(request, env) {
    const url = new URL(request.url)
    const APY_SERVER_URL = (env.APY_SERVER_URL || 'http://52.211.137.158:2737').replace(/\/$/, '')
    const ADMIN_PASSWORD = env.ADMIN_PASSWORD || 'change-me-in-production'

    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    }

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders })
    }

    const sendJson = (status, data) =>
      new Response(JSON.stringify(data), {
        status,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      })

    // API: /api/*
    if (url.pathname.startsWith('/api/')) {
      const subpath = url.pathname.replace(/^\/api/, '') || '/'

      if (request.method === 'GET' && subpath === '/health') {
        return sendJson(200, { status: 'ok', timestamp: new Date().toISOString() })
      }

      if (request.method === 'POST' && subpath === '/translate') {
        try {
          const contentType = request.headers.get('content-type') || ''
          let text, langpair

          if (contentType.includes('application/x-www-form-urlencoded')) {
            const formData = await request.formData()
            text = formData.get('q')
            langpair = formData.get('langpair')
          } else {
            const body = await request.json().catch(() => ({}))
            text = body?.text
            const direction = body?.direction
            langpair = direction === 'ido-epo' ? 'ido|epo' : 'epo|ido'
          }

          if (!text || !langpair) {
            return sendJson(400, { error: 'Missing text or langpair' })
          }

          const res = await fetch(`${APY_SERVER_URL}/translate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ q: text, langpair }),
          })

          if (!res.ok) {
            const errorText = await res.text().catch(() => 'No error body')
            return sendJson(502, {
              error: 'Translation service error',
              details: `APY server returned ${res.status}`,
              apyUrl: APY_SERVER_URL,
              errorBody: errorText,
            })
          }

          const data = await res.json()
          return sendJson(200, {
            translation: data.responseData?.translatedText || text,
            sourceLanguage: langpair.split('|')[0],
            targetLanguage: langpair.split('|')[1],
          })
        } catch (e) {
          return sendJson(500, { error: 'Translation service unavailable', details: e?.message })
        }
      }

      if (request.method === 'POST' && subpath === '/translate-url') {
        try {
          const body = await request.json().catch(() => ({}))
          const pageUrl = body?.url
          const direction = body?.direction
          if (!pageUrl || !direction) return sendJson(400, { error: 'Missing URL or direction' })

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
        try {
          const body = await request.json().catch(() => ({}))
          if (body?.password !== ADMIN_PASSWORD) return sendJson(401, { error: 'Invalid admin password' })
          return sendJson(200, { status: 'initiated', message: 'Rebuild requested (placeholder).' })
        } catch (e) {
          return sendJson(500, { error: 'Rebuild failed', details: e?.message })
        }
      }

      return sendJson(404, { error: 'API endpoint not found' })
    }

    // Static assets via ASSETS binding; fallback to index.html for SPA routing
    try {
      const asset = await env.ASSETS.fetch(request)
      return asset
    } catch (_) {
      try {
        const indexRequest = new Request(new URL('/index.html', request.url), request)
        return await env.ASSETS.fetch(indexRequest)
      } catch {
        return new Response('404 Not Found', { status: 404 })
      }
    }
  },
}

function extractTextFromHtml(html) {
  return html
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, ' ')
    .replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .substring(0, 5000)
}


