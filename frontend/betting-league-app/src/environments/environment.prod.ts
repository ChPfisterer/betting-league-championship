export const environment = {
  production: true,
  apiUrl: 'https://api.betting-platform.com',
  keycloak: {
    url: 'https://auth.betting-platform.com',
    realm: 'betting-platform',
    clientId: 'betting-frontend'
  },
  fontawesome: {
    kitId: '{{FONTAWESOME_KIT_ID}}' // Will be replaced during build with environment variable
  }
};