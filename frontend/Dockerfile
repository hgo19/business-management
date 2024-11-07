FROM node:18-alpine AS builder

WORKDIR /app

COPY package.json yarn.lock* package-lock.json* ./

RUN npm install --frozen-lockfile

COPY . .

RUN npm run build

FROM node:18-alpine AS runner

WORKDIR /app

COPY package.json yarn.lock* package-lock.json* ./
RUN npm install --only=production --frozen-lockfile

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

EXPOSE 3000

ENV NODE_ENV=production

CMD ["npm", "start"]
