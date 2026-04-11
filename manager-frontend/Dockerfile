FROM node:22-alpine
WORKDIR /app
COPY --chown=node:node package.json package-lock.json ./
RUN npm ci
COPY --chown=node:node . .
USER node
EXPOSE 5173
CMD ["npm", "run", "dev-api", "--", "--host"]
