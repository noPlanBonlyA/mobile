const { createProxyMiddleware } = require('http-proxy-middleware');

const target = process.env.REACT_APP_PROXY_TARGET || 'http://localhost:8080';

module.exports = function setupProxy(app) {
  const proxyOptions = {
    target,
    changeOrigin: true,
    secure: false,
  };

  app.use('/api', createProxyMiddleware(proxyOptions));
  app.use('/media', createProxyMiddleware(proxyOptions));
  app.use('/uploads', createProxyMiddleware(proxyOptions));
};
