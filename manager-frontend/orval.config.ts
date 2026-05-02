import { defineConfig } from 'orval';

export default defineConfig({
  netconf: {
    output: {
      mode: 'tags-split',
      target: 'src/api/',
      schemas: 'src/api/model',
      client: 'react-query',
      mock: true,
      clean: true,
    },
    input: {
      target: '/shared/openapi.json',
    },
  },
});
