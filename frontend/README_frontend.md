# Frontend for Smart Fraud Detection System

This directory contains the Vite + React frontend for communicating with the fraud detection backend.

## Setup

1. Make sure you have Node.js installed.
2. Install dependencies:
   ```bash
   npm install
   ```

## Development Server

Start the Vite development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`. Make sure the FastAPI backend is running simultaneously on `http://localhost:8000`.

## Building for Production

To create a production build:

```bash
npm run build
```
The optimized files will be generated in the `dist/` directory, ready to be deployed to Vercel, Netlify, or any static hosting service.
