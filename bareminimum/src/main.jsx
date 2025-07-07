import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import { createGlobalStyle } from 'styled-components'
import { globalStyles } from './design-tokens'
import { Toaster } from 'react-hot-toast'

const GlobalStyle = createGlobalStyle`${globalStyles}`

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <GlobalStyle />
    <App />
    <Toaster 
      position="bottom-center"
      toastOptions={{
        duration: 3000,
        style: {
          background: '#000',
          color: '#fff',
          fontSize: '14px',
          fontWeight: 700,
          textTransform: 'uppercase'
        }
      }}
    />
  </React.StrictMode>
)