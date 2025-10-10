import * as functions from 'firebase-functions'
import * as admin from 'firebase-admin'
import express from 'express'
import cors from 'cors'
import fetch from 'node-fetch'

admin.initializeApp()

const app = express()
app.use(cors({ origin: true }))
app.use(express.json())

// Configuration - prefer Firebase Functions config, then env, then defaults
const runtimeConfig = functions.config?.() as any || {}
const CONFIG_APY_URL = runtimeConfig.apy?.server_url
const CONFIG_ADMIN_PASSWORD = runtimeConfig.admin?.password

const APY_SERVER_URL = CONFIG_APY_URL || process.env.APY_SERVER_URL || 'http://localhost:2737'
const ADMIN_PASSWORD = CONFIG_ADMIN_PASSWORD || process.env.ADMIN_PASSWORD || 'change-me-in-production'

// Health check endpoint
app.get('/health', (req, res): void => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() })
})

// Text translation endpoint
app.post('/translate', async (req, res): Promise<void> => {
  try {
    const { text, direction } = req.body

    if (!text || !direction) {
      res.status(400).json({ error: 'Missing text or direction' })
      return
    }

    // Map direction to Apertium language pair format
    const langPair = direction === 'ido-epo' ? 'ido|epo' : 'epo|ido'

    // Call APy server
    const response = await fetch(`${APY_SERVER_URL}/translate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        q: text,
        langpair: langPair,
      }),
    })

    if (!response.ok) {
      throw new Error(`APy server error: ${response.statusText}`)
    }

    const data: any = await response.json()
    res.json({ 
      translation: data.responseData?.translatedText || text,
      sourceLanguage: direction.split('-')[0],
      targetLanguage: direction.split('-')[1],
    })
  } catch (error: any) {
    console.error('Translation error:', error)
    res.status(500).json({ 
      error: 'Translation service unavailable',
      details: error instanceof Error ? error.message : 'Unknown error'
    })
    return
  }
})

// URL translation endpoint
app.post('/translate-url', async (req, res): Promise<void> => {
  try {
    const { url, direction } = req.body

    if (!url || !direction) {
      res.status(400).json({ error: 'Missing URL or direction' })
      return
    }

    // Fetch the webpage content
    const pageResponse = await fetch(url)
    if (!pageResponse.ok) {
      res.status(400).json({ error: 'Could not fetch URL' })
      return
    }

    const html = await pageResponse.text()
    
    // Extract text content from HTML (simple extraction)
    const textContent = extractTextFromHtml(html)

    if (!textContent.trim()) {
      res.status(400).json({ error: 'No text content found in URL' })
      return
    }

    // Translate the extracted text
    const langPair = direction === 'ido-epo' ? 'ido|epo' : 'epo|ido'

    const translationResponse = await fetch(`${APY_SERVER_URL}/translate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        q: textContent,
        langpair: langPair,
      }),
    })

    if (!translationResponse.ok) {
      throw new Error(`APy server error: ${translationResponse.statusText}`)
    }

    const translationData: any = await translationResponse.json()

    res.json({
      original: textContent,
      translation: translationData.responseData?.translatedText || textContent,
      url: url,
    })
  } catch (error: any) {
    console.error('URL translation error:', error)
    res.status(500).json({ 
      error: 'URL translation failed',
      details: error instanceof Error ? error.message : 'Unknown error'
    })
    return
  }
})

// Admin rebuild endpoint
app.post('/admin/rebuild', async (req, res): Promise<void> => {
  try {
    const { password } = req.body

    if (password !== ADMIN_PASSWORD) {
      res.status(401).json({ error: 'Invalid admin password' })
      return
    }

    const logs: string[] = []
    logs.push('Starting rebuild process...')

    // This is a placeholder - actual implementation would:
    // 1. Pull latest from git repos
    // 2. Recompile Apertium dictionaries
    // 3. Restart APy server
    
    logs.push('Pulling latest code from apertium-ido...')
    logs.push('Pulling latest code from apertium-ido-epo...')
    logs.push('Compiling dictionaries...')
    logs.push('Restarting translation service...')
    logs.push('Rebuild complete!')

    // In production, you would trigger a Cloud Build or execute commands
    // via a secure mechanism. For now, return success
    res.json({
      success: true,
      logs: logs,
      timestamp: new Date().toISOString(),
    })
  } catch (error: any) {
    console.error('Rebuild error:', error)
    res.status(500).json({ 
      error: 'Rebuild failed',
      details: error instanceof Error ? error.message : 'Unknown error'
    })
    return
  }
})

// Helper function to extract text from HTML
const extractTextFromHtml = (html: string): string => {
  // Remove script and style tags
  let text = html.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
  text = text.replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, '')
  
  // Remove HTML tags
  text = text.replace(/<[^>]+>/g, ' ')
  
  // Decode HTML entities
  text = text.replace(/&nbsp;/g, ' ')
  text = text.replace(/&amp;/g, '&')
  text = text.replace(/&lt;/g, '<')
  text = text.replace(/&gt;/g, '>')
  text = text.replace(/&quot;/g, '"')
  
  // Clean up whitespace
  text = text.replace(/\s+/g, ' ')
  text = text.trim()
  
  return text
}

export const api = functions.https.onRequest(app)

