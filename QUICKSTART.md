# Quick Start Guide

## 🚀 Local Development (5 minutes)

### Step 1: Install Dependencies
```bash
# Install Node packages
npm install

# Install Python packages
pip install -r requirements.txt
```

### Step 2: Start Development Servers

**Terminal 1 - Frontend (React dev server with hot reload):**
```bash
npm run dev
```
→ Opens at http://localhost:5173

**Terminal 2 - Backend (Flask API):**
```bash
python app.py
```
→ Running at http://localhost:5000

### Step 3: Upload and Test
- Go to http://localhost:5173
- Drop an image or video file
- See instant AI detection results! 🎉

---

## 🌐 Deploy to Render (10 minutes)

### Prerequisites
✅ GitHub account  
✅ Render account (https://render.com - free tier available)  
✅ Code pushed to GitHub

### Step-by-Step Deployment

1. **Push your code to GitHub**
```bash
git add .
git commit -m "TypeScript frontend with Render deployment"
git push origin main
```

2. **Go to Render Dashboard**
   - https://dashboard.render.com
   - Click "New +" → "Web Service"

3. **Connect Your Repository**
   - Select your GitHub repo
   - Choose main branch
   - Authorize Render to access your repo

4. **Configure Service**
   - **Name:** `deepfake-detection` (or your choice)
   - **Runtime:** Python 3
   - **Build Command:** `bash build.sh`
   - **Start Command:** `gunicorn app:app`
   - **Instance:** Standard (free tier works, but may be slow)

5. **Click Deploy**
   - Wait 10-15 minutes for build
   - ✅ Service will be live at `https://deepfake-detection-xxx.onrender.com`

---

## 📁 Project Files Overview

| File | Purpose |
|------|---------|
| `src/App.tsx` | Main React component with state management |
| `src/components/` | Reusable UI components |
| `src/config.ts` | API endpoint configuration |
| `src/index.css` | Global styles + Tailwind |
| `app.py` | Flask backend API |
| `detector.py` | Deepfake detection model |
| `package.json` | Node dependencies & scripts |
| `vite.config.ts` | Frontend build configuration |
| `Procfile` | Render deployment configuration |
| `requirements.txt` | Python dependencies |

---

## 🎨 Design Features

✨ **Modern Blue Theme** (replacing purple)
- Gradient blue background: #0ea5e9 → #0284c7
- Clean white cards with shadow effects
- Responsive grid layout

📱 **Fully Responsive**
- Mobile-first design
- Works on all screen sizes
- Touch-friendly upload area

⚡ **Fast & Interactive**
- Drag & drop file upload
- Real-time detection results
- Loading animations
- Error handling

---

## 🔧 Customization

### Change Colors
Edit `tailwind.config.js` primary colors:
```js
colors: {
  primary: {
    500: '#0ea5e9',  // Main blue
    600: '#0284c7',  // Darker blue
    // ... etc
  }
}
```

### Change App Name/Text
Edit `src/components/Header.tsx`:
```tsx
<h1 className="text-white text-xl font-bold">Your App Name</h1>
```

### Change API Endpoint
Edit `src/config.ts`:
```ts
production: {
  apiUrl: 'https://your-api.com',
}
```

---

## 📊 Monitoring (After Deployment)

**Check Render Logs:**
- Dashboard → Your Service → Logs tab
- See real-time API calls
- Debug deployment issues

**Common Issues:**
- ❌ "Model file not found" → Ensure `deepfake_detector_best.pth` in repo
- ❌ "CORS error" → Check Flask CORS config in `app.py`
- ❌ "Connection refused" → Service might be spinning up (wait 30 sec)

---

## 💡 Pro Tips

1. **For faster Render builds:** Use GitHub Actions to pre-build frontend
2. **For better performance:** Add image/video compression before upload
3. **For scaling:** Consider upgrading Render instance type
4. **For data:** Add a database to store detection history

---

## 🐛 Troubleshooting

**Frontend not showing?**
```bash
npm run build  # Rebuild frontend
git push       # Push to GitHub
```

**API not responding?**
```bash
# Check locally first
curl http://localhost:5000/api/health

# Check Render logs for errors
```

**Build fails on Render?**
- Check build logs in Render dashboard
- PyTorch installation takes time (~3-5 min)
- Free tier may timeout - upgrade instance if needed

---

## 📚 Next Steps

- [ ] Add user authentication
- [ ] Create API rate limiting  
- [ ] Add detection history
- [ ] Build admin dashboard
- [ ] Add webhook notifications
- [ ] Deploy on custom domain

---

**Questions?** Check DEPLOYMENT_GUIDE.md for more details! 🚀
