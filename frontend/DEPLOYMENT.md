# Medical Research Assistant - Frontend Deployment Guide

## Deploy to Render

### Step 1: Push Your Code to GitHub
```bash
cd c:\Users\HP\Desktop\Medical_Research_RAG
git add .
git commit -m "Add frontend production environment config"
git push
```

### Step 2: Create a New Static Site on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Static Site"**
3. Connect your GitHub repository: `Medical-Research-Assistant-RAG-`
4. Configure the following settings:

   **Basic Settings:**
   - **Name:** `medical-research-frontend` (or your preferred name)
   - **Branch:** `main`
   - **Root Directory:** `frontend/med-scholar-ai`

   **Build Settings:**
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`

   **Environment Variables:**
   - Add: `VITE_API_BASE_URL` = `https://medical-research-assistant-rag.onrender.com`

5. Click **"Create Static Site"**

### Step 3: Wait for Deployment

Render will:
- Install dependencies (`npm install`)
- Build your React app (`npm run build`)
- Deploy the static files
- Give you a URL like: `https://medical-research-frontend.onrender.com`

### Step 4: Update Backend CORS (Important!)

Your backend currently allows all origins (`allow_origins=["*"]`), which works for testing but update it for production if needed.

If you want to restrict CORS to your frontend URL only, update `backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "https://medical-research-frontend.onrender.com"  # Your frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then redeploy your backend.

---

## Alternative: Deploy to Vercel (Faster & Free)

Vercel is optimized for React/Vite apps and has faster builds:

1. Go to [Vercel](https://vercel.com)
2. Click **"Add New Project"**
3. Import your GitHub repo
4. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend/med-scholar-ai`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Environment Variables:**
     - `VITE_API_BASE_URL` = `https://medical-research-assistant-rag.onrender.com`
5. Click **"Deploy"**

---

## Alternative: Deploy to Netlify

1. Go to [Netlify](https://app.netlify.com)
2. Click **"Add new site"** → **"Import an existing project"**
3. Connect GitHub repo
4. Configure:
   - **Base directory:** `frontend/med-scholar-ai`
   - **Build command:** `npm run build`
   - **Publish directory:** `dist`
   - **Environment variables:**
     - `VITE_API_BASE_URL` = `https://medical-research-assistant-rag.onrender.com`
5. Click **"Deploy site"**

---

## Testing Your Deployment

Once deployed, test:
1. Open your frontend URL
2. Try a query: "What are current treatments for Type 2 Diabetes?"
3. Check browser console for any CORS/API errors
4. Test file upload functionality

---

## Troubleshooting

**CORS Errors:**
- Ensure backend `allow_origins` includes your frontend URL
- Check browser console for error details

**API Connection Fails:**
- Verify `VITE_API_BASE_URL` environment variable is set correctly
- Ensure backend is running at `https://medical-research-assistant-rag.onrender.com/docs`

**Build Fails:**
- Check Node.js version (Render uses latest by default)
- Review build logs in Render dashboard
- Try building locally: `npm run build`

---

## Recommended: Use Render for Both

Since your backend is already on Render, deploying the frontend there keeps everything in one place. However, **Vercel** and **Netlify** typically have faster static site deployments and better CDN performance.

**My Recommendation:** Use **Vercel** for frontend (faster, better DX) + **Render** for backend.
