# OUSSAMA SAT PRO AI

A mobile firmware flasher for satellite receivers — select a `.bin` file, connect a USB device, and flash firmware with real-time progress tracking.

## Run & Operate

- `pnpm --filter @workspace/mobile run dev` — run the Expo dev server (mobile)
- `pnpm --filter @workspace/api-server run dev` — run the API server (port 8080)
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- No required env vars for the mobile app (frontend-only, AsyncStorage for state)

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- Mobile: Expo SDK 54, Expo Router (file-based routing), React Native 0.81
- API: Express 5 (not used by mobile in first build)
- DB: PostgreSQL + Drizzle ORM (not used in first build)
- Fonts: Inter (400/500/600/700) via @expo-google-fonts/inter
- File picker: expo-document-picker ~14.0.8
- Icons: @expo/vector-icons (Feather + MaterialCommunityIcons)

## Where things live

- `artifacts/mobile/` — Expo mobile app
- `artifacts/mobile/app/index.tsx` — main firmware flash screen (single-screen app)
- `artifacts/mobile/constants/colors.ts` — dark theme tokens (primary #00CC66, accent #8800BB)
- `artifacts/mobile/app/_layout.tsx` — root layout (no tabs, single Stack)
- `artifacts/api-server/` — Express API server (health check only for now)
- `lib/api-spec/openapi.yaml` — OpenAPI contract (source of truth)

## Architecture decisions

- **Single-screen app**: No tab bar — firmware flashing is a linear workflow (select → connect → flash), not a multi-section app.
- **Frontend-only**: All state is component-local (no AsyncStorage needed — no persistence required for a flashing tool).
- **WebSerial API on web**: On Chrome, real USB serial communication via `navigator.serial`. On native Expo Go, USB OTG requires a custom native build (shown as a platform notice).
- **Dark theme only**: App is tool-oriented; the original Python/Kivy design used a dark background with green accents — maintained in the Expo port.
- **Animated LED**: React Native `Animated` loop for the pulsing green LED when a device is connected, matching the original Kivy animation.

## Product

- Select a `.bin` firmware file from the device storage
- Connect a USB serial device (WebSerial on Chrome web; platform notice on native)
- Animated LED status indicator with pulsing effect when connected
- Real-time progress bar during firmware transfer
- Platform detection: WebSerial (Chrome), native notice for Expo Go

## User preferences

_Populate as you build._

## Gotchas

- `expo-document-picker` must be pinned to `~14.0.8` (Expo SDK 54 compatibility)
- WebSerial API is Chrome-only; not available in Safari or Firefox
- USB OTG on native requires a custom Expo build with `usbserial4a` equivalent native module
- Do NOT use `"usb"` as a Feather icon name — it's invalid; use `"link-2"` instead

## Pointers

- See the `expo` skill for mobile architecture guidelines
- See the `pnpm-workspace` skill for workspace structure details
