const AUTH_TYPE = process.env.AUTH_TYPE || 'bearer';

function getAuthHeader() {
  if (AUTH_TYPE === 'basic') {
    const user = process.env.BASIC_USER || '';
    const pass = process.env.BASIC_PASS || '';
    const encoded = Buffer.from(`${user}:${pass}`).toString('base64');
    return `Basic ${encoded}`;
  }

  return process.env.BEARER_TOKEN || require('./token').token;
}

module.exports = { getAuthHeader };
