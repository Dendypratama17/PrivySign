import http from 'k6/http';
import { check, sleep } from 'k6';
import { token } from './config/token.js';
import { BASE_URL } from './config/env.js';
import { htmlReport } from 'https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js';

export function handleSummary(data) {
  return {
    'summary.html': htmlReport(data),
  };
}

export const options = {
  vus: 50,
  duration: '30s',

  thresholds: {
    http_req_duration: ['p(95)<5000'],
  },
};

function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(
    /[xy]/g,
    function (c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x'
        ? r
        : (r & 0x3 | 0x8);

      return v.toString(16);
    }
  );
}

const endpoint =
  `${BASE_URL}/privysign/v1/users/subscriptions/status`;

export default function () {

  const headers = {
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json',
    'X-Application-Name': 'PrivySign',
    'X-Platform-Name': 'API',
    'X-Platform-Type': 'Automation API',
    'X-Request-ID': uuidv4(),
    'X-Application-Version': '0.0.0.1',
  };

  const res = http.get(endpoint, {
    headers,
  });

  let body = {};

  try {
    body = JSON.parse(res.body);
  } catch (e) {
    console.log('Failed parse JSON response');
    console.log(res.body);
  }

  check(res, {
    'status is 200': (r) =>
      r.status === 200,

    'message is valid': () =>
      body.message ===
      'orchestrator-privysign.success.users.subscriptions.status',
  });

  console.log(`
    ====================================
    REQUEST ID    : ${headers['X-Request-ID']}
    RESPONSE TIME : ${res.timings.duration} ms
    STATUS        : ${res.status}
    MESSAGE       : ${body.message}
    ====================================
  `);

  sleep(1);
}