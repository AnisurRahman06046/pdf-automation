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

  const handlePdfChange = async (e) => {
    const file = e.target.files[0]
    if (file) {
      setPdfFile(file)
      setDownloadUrl(null)
      setStatus('Analyzing PDF form fields...')

      // Get PDF fields
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
    setStatus('Processing... Extracting text from images...')
    setDownloadUrl(null)

    try {
      // Step 1: OCR the images
      const ocrFormData = new FormData()
      images.forEach(img => ocrFormData.append('images', img))

      const ocrResponse = await fetch(`${API_URL}/api/ocr/extract-parsed`, {
        method: 'POST',
        body: ocrFormData
      })

      if (!ocrResponse.ok) {
        throw new Error('OCR failed: ' + (await ocrResponse.json()).detail)
      }

      const ocrData = await ocrResponse.json()
      setOcrResults(ocrData)
      setStatus('OCR complete. Filling PDF...')

      // Step 2: Build field mapping (map PDF fields to parsed data)
      const fieldMapping = {}
      const parsed = ocrData.parsed_data

      pdfFields.forEach((field, index) => {
        const fieldName = field.name.toLowerCase()

        if (fieldName.includes('name') && parsed.names.length > 0) {
          fieldMapping[field.name] = 'names[0]'
        } else if ((fieldName.includes('date') || fieldName.includes('dob') || fieldName.includes('birth')) && parsed.dates.length > 0) {
          fieldMapping[field.name] = 'dates[0]'
        } else if ((fieldName.includes('id') || fieldName.includes('number') || fieldName.includes('passport') || fieldName.includes('nid')) && parsed.id_numbers.length > 0) {
          fieldMapping[field.name] = 'id_numbers[0]'
        } else if (fieldName.includes('email') && parsed.emails.length > 0) {
          fieldMapping[field.name] = 'emails[0]'
        } else if ((fieldName.includes('phone') || fieldName.includes('mobile') || fieldName.includes('tel')) && parsed.phone_numbers.length > 0) {
          fieldMapping[field.name] = 'phone_numbers[0]'
        } else if (fieldName.includes('address') && parsed.addresses.length > 0) {
          fieldMapping[field.name] = 'addresses[0]'
        }
      })

      // Step 3: Fill the PDF using /api/process
      const processFormData = new FormData()
      processFormData.append('pdf_file', pdfFile)
      images.forEach(img => processFormData.append('images', img))
      processFormData.append('field_mapping', JSON.stringify(fieldMapping))

      const fillResponse = await fetch(`${API_URL}/api/process`, {
        method: 'POST',
        body: processFormData
      })

      if (!fillResponse.ok) {
        throw new Error('PDF fill failed: ' + (await fillResponse.json()).detail)
      }

      const blob = await fillResponse.blob()
      const url = URL.createObjectURL(blob)
      setDownloadUrl(url)
      setStatus('PDF filled successfully! Click download to get your file.')

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
        <p>PDF Automation API</p>
      </footer>
    </div>
  )
}

export default App
