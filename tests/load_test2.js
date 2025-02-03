import http from 'k6/http';
import { sleep } from 'k6';

// setup
export let options = {
  stages: [
    { duration: '10s', target: 1 }, // 1 user per 30 10 sec
    { duration: '20s', target: 2 }, // 2u per 20s
    { duration: '20s', target: 3 }, // 3u per 20s 
    { duration: '10s', target: 0 }, // 0u per 10s
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% requests in 500 ms
  },
};

// main func for every user
export default function () {
  const res = http.get('https://test.k6.io');
  if (res.status !== 200) {
    console.error(`Request failed. Status: ${res.status}`);
  }
  sleep(1); // pause
}
