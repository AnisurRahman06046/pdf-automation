import { useState } from 'react'
import './App.css'

const API_URL = 'http://localhost:8000'

function App() {
  const [pdfFile, setPdfFile] = useState(null)
  const [images, setImages] = useState([])
  const [pdfFields, setPdfFields] = useState([])
  const [status, setStatus] = useState('')
  const [loading, setLoading] = useState(false)
  const [downloadUrl, setDownloadUrl] = useState(null)
  const [ocrResults, setOcrResults] = useState(null)
  const [language, setLanguage] = useState('eng')

  const handlePdfChange = async (e) => {
    const file = e.target.files[0]
    if (file) {
      setPdfFile(file)
      setDownloadUrl(null)
      setStatus('Analyzing PDF form fields...')

      const formData = new FormData()
      formData.append('pdf_file', file)

      try {
        const response = await fetch(`${API_URL}/api/pdf/fields`, {
          method: 'POST',
          body: formData
        })
        const data = await response.json()
        setPdfFields(data.fields || [])
        setStatus(`Found ${data.field_count} fillable fields in PDF`)
      } catch (error) {
        setStatus('Error analyzing PDF: ' + error.message)
      }
    }
  }

  const handleImagesChange = (e) => {
    const files = Array.from(e.target.files)
    setImages(files)
    setDownloadUrl(null)
    setOcrResults(null)
    setStatus(`Selected ${files.length} image(s) for OCR`)
  }

  const handleAutoFill = async () => {
    if (!pdfFile) {
      setStatus('Please upload a PDF form first')
      return
    }
    if (images.length === 0) {
      setStatus('Please upload at least one image')
      return
    }

    setLoading(true)
    setStatus('Processing... Smart matching fields...')
    setDownloadUrl(null)

    try {
      // Use the smart auto-fill endpoint
      const formData = new FormData()
      formData.append('pdf_file', pdfFile)
      images.forEach(img => formData.append('images', img))
      formData.append('language', language)

      const response = await fetch(`${API_URL}/api/auto-fill`, {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Auto-fill failed')
      }

      const fieldsFilled = response.headers.get('X-Fields-Filled') || '?'
      const totalFields = response.headers.get('X-Total-Fields') || '?'

      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      setDownloadUrl(url)
      setStatus(`PDF filled successfully! ${fieldsFilled}/${totalFields} fields filled.`)

      // Also get OCR results for display
      const ocrFormData = new FormData()
      images.forEach(img => ocrFormData.append('images', img))
      ocrFormData.append('language', language)

      const ocrResponse = await fetch(`${API_URL}/api/ocr/extract-parsed`, {
        method: 'POST',
        body: ocrFormData
      })

      if (ocrResponse.ok) {
        const ocrData = await ocrResponse.json()
        setOcrResults(ocrData)
      }

    } catch (error) {
      setStatus('Error: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = () => {
    if (downloadUrl) {
      const a = document.createElement('a')
      a.href = downloadUrl
      a.download = `filled_${pdfFile.name}`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
    }
  }

  return (
    <div className="app">
      <header>
        <h1>PDF Auto-Fill</h1>
        <p>Upload a PDF form and images to automatically fill the form using OCR</p>
      </header>

      <main>
        <div className="settings-section">
          <div className="setting">
            <label htmlFor="language">OCR Language:</label>
            <select
              id="language"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
            >
              <option value="eng">English</option>
              <option value="ita">Italian</option>
              <option value="eng+ita">English + Italian</option>
            </select>
          </div>
        </div>

        <div className="upload-section">
          <div className="upload-box">
            <h2>1. Upload PDF Form</h2>
            <input
              type="file"
              accept=".pdf"
              onChange={handlePdfChange}
              id="pdf-input"
            />
            <label htmlFor="pdf-input" className="file-label">
              {pdfFile ? pdfFile.name : 'Choose PDF file'}
            </label>

            {pdfFields.length > 0 && (
              <div className="fields-list">
                <h4>Detected Fields:</h4>
                <ul>
                  {pdfFields.map((field, i) => (
                    <li key={i}>{field.name} ({field.field_type})</li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          <div className="upload-box">
            <h2>2. Upload Images</h2>
            <p className="hint">NID, Passport, Documents for OCR</p>
            <input
              type="file"
              accept="image/*"
              multiple
              onChange={handleImagesChange}
              id="images-input"
            />
            <label htmlFor="images-input" className="file-label">
              {images.length > 0 ? `${images.length} image(s) selected` : 'Choose images'}
            </label>

            {images.length > 0 && (
              <div className="image-preview">
                {images.map((img, i) => (
                  <span key={i} className="image-name">{img.name}</span>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="action-section">
          <button
            className="auto-fill-btn"
            onClick={handleAutoFill}
            disabled={loading || !pdfFile || images.length === 0}
          >
            {loading ? 'Processing...' : 'Auto Fill PDF'}
          </button>

          {downloadUrl && (
            <button className="download-btn" onClick={handleDownload}>
              Download Filled PDF
            </button>
          )}
        </div>

        {status && (
          <div className={`status ${downloadUrl ? 'success' : ''}`}>
            {status}
          </div>
        )}

        {ocrResults && (
          <div className="ocr-results">
            <h3>Extracted Data</h3>
            <div className="parsed-data">
              {ocrResults.parsed_data.names.length > 0 && (
                <p><strong>Names:</strong> {ocrResults.parsed_data.names.join(', ')}</p>
              )}
              {ocrResults.parsed_data.dates.length > 0 && (
                <p><strong>Dates:</strong> {ocrResults.parsed_data.dates.join(', ')}</p>
              )}
              {ocrResults.parsed_data.id_numbers.length > 0 && (
                <p><strong>ID Numbers:</strong> {ocrResults.parsed_data.id_numbers.join(', ')}</p>
              )}
              {ocrResults.parsed_data.emails.length > 0 && (
                <p><strong>Emails:</strong> {ocrResults.parsed_data.emails.join(', ')}</p>
              )}
              {ocrResults.parsed_data.phone_numbers.length > 0 && (
                <p><strong>Phones:</strong> {ocrResults.parsed_data.phone_numbers.join(', ')}</p>
              )}
              {ocrResults.parsed_data.addresses.length > 0 && (
                <p><strong>Addresses:</strong> {ocrResults.parsed_data.addresses.join(', ')}</p>
              )}
            </div>
          </div>
        )}
      </main>

      <footer>
        <p>PDF Automation API - Smart Pattern Matching</p>
      </footer>
    </div>
  )
}

export default App
