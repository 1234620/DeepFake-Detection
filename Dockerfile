# Stage 1: Build the React frontend
FROM node:18 AS frontend-builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Build the Python backend
FROM python:3.10-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files and built frontend
COPY . .
COPY --from=frontend-builder /app/dist ./dist

# Set production environment so Flask serves the built React app
ENV ENVIRONMENT=production

EXPOSE 5000

CMD ["python", "app.py"]
