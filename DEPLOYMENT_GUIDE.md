# DeepFake Detection - TypeScript Frontend with Render Deployment Guide

## Project Structure

```
deepfake-detection/
├── src/                          # TypeScript React source code
│   ├── components/
│   │   ├── FileUpload.tsx       # File upload component
│   │   ├── DetectionResult.tsx  # Results display
│   │   ├── Features.tsx         # Feature cards
│   │   └── Header.tsx           # Navigation header
│   ├── App.tsx                  # Main app component
│   ├── main.tsx                 # React entry point
│   └── index.css                # Global styles with Tailwind
├── dist/                        # Built frontend (generated)
├── app.py                       # Flask backend (updated for Render)
├── detector.py                  # Deepfake detection model
├── model.py                     # Model architecture
├── package.json                 # Node dependencies
├── vite.config.ts               # Vite build config
├── tsconfig.json                # TypeScript config
├── tailwind.config.js           # Tailwind CSS config
├── Procfile                     # Render deployment config
├── build.sh                     # Build script
└── requirements.txt             # Python dependencies
```

## Setup Instructions

### Local Development

1. **Install Node dependencies:**
   ```bash
   npm install
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start development server (in separate terminals):**
   
   Terminal 1 - Frontend dev server:
   ```bash
   npm run dev
   ```
   
   Terminal 2 - Backend:
   ```bash
   python app.py
   ```

4. **Access the application:**
   - Frontend: http://localhost:5173
   - API: http://localhost:5000

### Building for Production

```bash
npm run build
```

This creates a `dist/` folder with optimized frontend assets.

## Render Deployment

### Prerequisites
- Render account (https://render.com)
- GitHub repository with your code
- PyTorch model file (`deepfake_detector_best.pth`) in repo root

### Deployment Steps

1. **Push code to GitHub:**
   ```bash
   git add .
   git commit -m "TypeScript frontend with Render setup"
   git push origin main
   ```

2. **Create new Web Service on Render:**
   - Go to https://dashboard.render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Choose the branch (main)

3. **Configure service:**
   - **Name:** deepfake-detection
   - **Environment:** Python 3
   - **Build Command:** `bash build.sh`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Standard (or higher if needed)

4. **Environment Variables (Optional):**
   - `RENDER=true` (auto-detected)
   - `PORT=5000` (auto-set)

5. **Deploy:**
   - Click "Deploy Service"
   - Wait for build to complete (5-10 minutes)
   - Your app will be live at `https://your-service-name.onrender.com`

### Important Notes for Render

- **Build Duration:** First build may take 10+ minutes due to PyTorch installation
- **Upload Folder:** Uses `/tmp/uploads` (cleared on redeploy)
- **Static Files:** Frontend automatically served from `dist/` folder
- **Free Tier:** Services spin down after 15 minutes of inactivity
- **CORS:** Configured to work with hosted frontend

## Features

✨ **Modern UI Design** - Professional interface inspired by AI Resume Builder
🎨 **Blue Color Scheme** - Clean blue gradient replacing purple
📁 **Drag & Drop** - Easy file upload interface
⚡ **Real-time Detection** - Fast AI model inference
📊 **Confidence Scores** - Detailed detection results
🔒 **Secure Processing** - Files not permanently stored
📱 **Responsive** - Works on desktop and mobile

## Technology Stack

**Frontend:**
- React 18
- TypeScript
- Vite (build tool)
- Tailwind CSS (styling)
- Lucide React (icons)

**Backend:**
- Flask (Python web framework)
- PyTorch (ML model)
- Gunicorn (production server)

**Deployment:**
- Render (hosting)
- GitHub (version control)

## Troubleshooting

### Build fails with PyTorch error
- PyTorch is heavy (200MB+)
- First build takes time - be patient
- Check Render logs for specific errors

### Frontend not loading
- Ensure `npm run build` completes successfully
- Check that `dist/` folder is created
- Verify static file serving in `app.py`

### API calls return CORS error
- CORS is configured in Flask
- Check browser console for exact error
- Verify API URL in `.env` or frontend code

### Model file not found
- Ensure `deepfake_detector_best.pth` is in repo root
- Git LFS might be needed for large files (>100MB)

## Performance Tips

1. **Optimize Model Loading:** Cache model in memory
2. **Limit File Size:** 100MB max (configured)
3. **Use Compression:** Gzip frontend assets
4. **CDN:** Render provides automatic CDN caching

## Future Enhancements

- [ ] Batch processing
- [ ] Video frame analysis
- [ ] API rate limiting
- [ ] User authentication
- [ ] Analytics dashboard
- [ ] Webhook support

## Support

For issues or questions:
1. Check Render logs: Dashboard → Service → Logs
2. Review Flask server logs locally
3. Check browser console for frontend errors
4. Verify model file exists and is readable
