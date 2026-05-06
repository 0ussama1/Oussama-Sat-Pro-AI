# GitHub Actions Setup — OUSSAMA SAT PRO AI

Follow these steps **once** to connect your GitHub repository to the automated APK builder.

---

## Step 1 — Push your project to GitHub

If you haven't already:

```bash
git init
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git add .
git commit -m "Initial commit"
git push -u origin main
```

---

## Step 2 — Add Repository Secrets

Go to your GitHub repository →  
**Settings → Secrets and variables → Actions → New repository secret**

Add these **4 secrets** exactly as shown:

| Secret name | Value |
|---|---|
| `KEYSTORE_BASE64` | *(paste the long string from Step 3 below)* |
| `KEYSTORE_PASSWORD` | `ZNf5D3L3PfO6Fa0BI8rGda` |
| `KEY_PASSWORD` | `ZNf5D3L3PfO6Fa0BI8rGda` |
| `KEYSTORE_ALIAS` | `oussama_sat` |

---

## Step 3 — Get the KEYSTORE_BASE64 value

Run this command in the `python-kivy/` directory to get the base64 keystore string to paste as the `KEYSTORE_BASE64` secret:

```bash
base64 -w 0 release.keystore
```

Copy the entire output (one long line) and paste it as the `KEYSTORE_BASE64` secret value.

> **Important:** Back up both `release.keystore` and `.keystore.env` somewhere safe
> (external drive, password manager, etc.). If you lose the keystore, you cannot
> update the app under the same package ID on the Play Store or sideloaded installs.

---

## Step 4 — Trigger a build

**Automatic:** Push any commit to `main` — the workflow starts immediately.

**Manual:** Go to  
**Actions → Build & Sign APK → Run workflow → Run workflow**

---

## Step 5 — Download the APK

1. Go to **Actions** in your GitHub repository
2. Click the completed workflow run
3. Scroll to **Artifacts** at the bottom
4. Download `oussama-sat-pro-ai-<sha>.zip`
5. Unzip → install the `.apk` on your Android device

---

## Step 6 — Create a versioned release (optional)

Tag a commit to automatically create a GitHub Release with the APK attached:

```bash
git tag v1.0
git push origin v1.0
```

The APK will appear under **Releases** in your repository, ready to share or distribute.

---

## Build times

| Run | Approximate time |
|---|---|
| First run (downloads SDK + NDK) | 25–40 minutes |
| Subsequent runs (cached SDK) | 8–15 minutes |

---

## Troubleshooting

- **Build failed?** Download the `build-log-<sha>` artifact from the failed run for full logs.
- **Signature error?** Make sure all 4 secrets are set and the `KEYSTORE_BASE64` value has no line breaks.
- **"No unsigned APK"?** The Buildozer step failed — check the build log artifact.
