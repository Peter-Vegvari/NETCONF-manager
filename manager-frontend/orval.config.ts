import { defineConfig } from 'orval';

export default defineConfig({
  petstore: {
    output: {
      mode: 'tags-split',
      target: 'src/api/',
      schemas: 'src/api/model',
      client: 'react-query',
      mock: true,
    },
    input: {
      target: 'http://manager-backend:8000/openapi.json',
    },
  },
});