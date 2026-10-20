# PulseView Vercel Dashboard

1. Push these files to GitHub.
2. Open https://vercel.com/new and import the repository.
3. Ensure the project root contains `app.py` and `requirements.txt`.
4. Deploy; Vercel supports Flask detection.
5. In Project Settings → Environment Variables, set `DEVICE_TOKEN` to a long random value and redeploy.

## API
- `POST /api/data` JSON: `{"heart_rate":76,"spo2":98}`
- `GET /api/latest`
- `GET /api/health`

When `DEVICE_TOKEN` is set, POST must include `X-Device-Token`.

## Important
This starter uses in-memory storage. Vercel serverless requests can run on different instances, so a POST and later GET may not see the same state. For a genuinely live dashboard, connect a shared database or realtime service and update the API to read/write through it.
