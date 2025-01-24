import http from 'k6/http';
import { sleep } from 'k6';

// Настраиваем сценарий
export let options = {
  stages: [
    { duration: '10s', target: 1 }, // 10 пользователей в течение первых 30 секунд
    { duration: '20s', target: 2 }, // Увеличение до 50 пользователей за 1 минуту
    { duration: '20s', target: 3 }, // Поддерживаем нагрузку с 50 пользователями 2 минуты
    { duration: '10s', target: 0 }, // Уменьшение нагрузки до 0 за 30 секунд
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% запросов должны завершаться за 500 мс
  },
};

// Основная функция, выполняемая каждым виртуальным пользователем
export default function () {
  const res = http.get('https://test.k6.io');
  if (res.status !== 200) {
    console.error(`Request failed. Status: ${res.status}`);
  }
  sleep(1); // Имитация паузы между запросами
}
