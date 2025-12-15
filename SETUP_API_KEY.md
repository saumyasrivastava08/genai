# How to Set Up Your OpenAI API Key

## Step 1: Get Your API Key from OpenAI

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Log in to your OpenAI account
3. Click **"Create new secret key"** or **"+ Create new secret key"**
4. Give it a name (e.g., "GenAI-Project")
5. **COPY THE KEY IMMEDIATELY** - you won't be able to see it again!
   - It will look like: `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## Step 2: Add the API Key to Your .env File

### Option A: Edit .env file in VS Code

1. Open the file: `.env` (in the project root)
2. Replace `your_openai_api_key_here` with your actual API key
3. Save the file

**Before:**
```
OPENAI_API_KEY=your_openai_api_key_here
```

**After:**
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Option B: Use PowerShell Command

Run this command in your terminal (replace with your actual key):

```powershell
(Get-Content .env) -replace 'your_openai_api_key_here', 'sk-proj-YOUR_ACTUAL_KEY_HERE' | Set-Content .env
```

## Step 3: Verify It Works

After adding your API key, run the application:

```powershell
python src/main.py
```

Then in another terminal, test it:

```powershell
python example_usage.py
```

Or use curl:

```powershell
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d "{\"question\":\"Hello, are you working?\"}"
```

## Important Security Notes

⚠️ **NEVER commit your .env file to version control!**

- The `.env` file is already in `.gitignore`
- Never share your API key publicly
- If you accidentally expose it, delete it immediately from OpenAI dashboard and create a new one

## Troubleshooting

### "OpenAI API key not configured" Error
- Make sure your `.env` file exists in the project root
- Check that the API key starts with `sk-`
- Restart the application after adding the key

### "Invalid API key" Error
- Verify you copied the entire key
- Check for extra spaces
- Make sure the key hasn't been deleted from OpenAI dashboard

### Check if API key is loaded:

```powershell
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Key loaded!' if os.getenv('OPENAI_API_KEY') else 'Key NOT loaded')"
```

## Quick Start After Setup

```powershell
# 1. Start the server
python src/main.py

# 2. In a new terminal, run examples
python example_usage.py

# 3. Or visit the API docs
# Open browser: http://localhost:8000/docs
```

---

**Need help?** Check the main [README.md](README.md) for more information.
