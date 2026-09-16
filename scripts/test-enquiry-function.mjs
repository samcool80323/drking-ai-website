import assert from 'node:assert/strict';
import { onRequestPost } from '../functions/api/enquiries.js';

const records = [];
const DB = {
  prepare(sql) {
    return {
      bind(...values) {
        return {
          async run() {
            records.push({ sql, values });
            return { success: true };
          },
        };
      },
    };
  },
};

const request = (body, headers = {}) => new Request('https://drking.ai/api/enquiries', {
  method: 'POST',
  headers: { Origin: 'https://drking.ai', 'Content-Type': 'application/json', ...headers },
  body: JSON.stringify(body),
});

const valid = await onRequestPost({
  request: request({
    type: 'demo-request',
    source: '/demo',
    pageTitle: 'Book a demo',
    fields: { name: 'Test Person', email: 'test@example.com', clinic: 'Test Clinic' },
  }),
  env: { DB },
  waitUntil() {},
});
assert.equal(valid.status, 201);
assert.equal(records.length, 1);
assert.equal(records[0].values[2], 'demo-request');
assert.equal(records[0].values[6], 'test@example.com');

const badEmail = await onRequestPost({
  request: request({ type: 'demo-request', source: '/demo', fields: { email: 'not-an-email' } }),
  env: { DB },
  waitUntil() {},
});
assert.equal(badEmail.status, 400);
assert.equal(records.length, 1);

const wrongOrigin = await onRequestPost({
  request: request({ type: 'demo-request', source: '/demo', fields: { name: 'Test', email: 'test@example.com' } }, { Origin: 'https://example.com' }),
  env: { DB },
  waitUntil() {},
});
assert.equal(wrongOrigin.status, 403);

const missingBinding = await onRequestPost({
  request: request({ type: 'demo-request', source: '/demo', fields: { name: 'Test', email: 'test@example.com' } }),
  env: {},
  waitUntil() {},
});
assert.equal(missingBinding.status, 503);

const unknownType = await onRequestPost({
  request: request({ type: 'unknown', source: '/demo', fields: { name: 'Test', email: 'test@example.com' } }),
  env: { DB },
  waitUntil() {},
});
assert.equal(unknownType.status, 400);
assert.equal(records.length, 1);

console.log('Enquiry function tests passed.');
