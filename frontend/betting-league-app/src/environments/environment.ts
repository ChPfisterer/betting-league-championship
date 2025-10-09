export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api/v1',  // Fixed: include API version prefix
  keycloak: {
    url: 'http://localhost:8090',
    realm: 'betting-platform',
    clientId: 'betting-frontend'
  },
  fontawesome: {
    kitId: '89974f2862' // This will be overridden by environment variable
  }
};