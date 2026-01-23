// Environment configuration for different deployment scenarios
export const config = {
  // Local development
  development: {
    apiUrl: 'http://localhost:5000',
    isDev: true,
  },
  // Render production
  production: {
    apiUrl: window.location.origin, // Same origin as frontend
    isDev: false,
  },
}

export const getConfig = () => {
  if (import.meta.env.DEV) {
    return config.development
  }
  return config.production
}
