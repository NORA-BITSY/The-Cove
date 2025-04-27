import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import AuthProvider from "./context/AuthContext";
import './index.css' // assuming Tailwind is imported here

ReactDOM.createRoot(document.getElementById('root')).render(
  <AuthProvider>
    <App />
  </AuthProvider>
)
