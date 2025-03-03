import http from 'k6/http';
import { check, sleep } from 'k6';
import { htmlReport } from    "https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js";


export let options = {
  vus: 1, // number of users
  duration: '30s', // test duration
};

export default function () {
  let res = http.get('https://test.k6.io');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1); // Pause
}

export function handleSummary(data) {
	return {
		'TestSummaryReport.html': htmlReport(data, { debug: true })
	};
}
