# ODYSSEY RPG — Complete Application & Feature Documentation

> **Comprehensive record of all features, architectural specifications, design systems, and workflow enhancements implemented in Odyssey from inception.**

---

## 🧭 Executive Overview

**Odyssey** (formerly IRIS Quest / Creative Vault) is an iOS-inspired, gamified personal productivity and identity transformation system. It bridges the gap between daily task execution, multi-month goal campaigns, intrinsic weekly reflection, and long-term identity evolution.

---

## 📱 1. Cross-Platform Responsive Layout & Design System

- **Apple / iOS Design Language**:
  - Translucent elevated cards (`var(--bg-card)`), glassmorphism borders (`var(--border-system)`), vibrant SF-style accent colors (Indigo `#5856D6`, Pink/Rose `#FF2D55`, Orange `#FF9500`, Emerald `#34C759`, Blue `#007AFF`).
  - Dark & Light Theme adaptivity with automatic system theme synchronization.
- **Adaptive Viewport Ratio**:
  - **Mobile (PWA)**: Optimized for 375px–430px single-column mobile view with safe-area padding for notches and home indicators.
  - **Tablet**: Fluid responsive grid layout (2-column cards, adaptive bottom nav).
  - **Desktop / Laptop**: Max-width centered fluid layout (640px–1000px) maintaining RPG card ergonomics on ultra-wide screens.
- **Progressive Web App (PWA)**:
  - Web App Manifest (`manifest.json`), custom icons (`icon-192.png`, `icon-512.png`), and standalone display mode detection.
  - Service Worker (`sw.js`) with Network-First strategy and cache-purging on version bumps.

---

## 🔐 2. Authentication, Profile Persistence & Database Sync

### A. Mandatory Auth Gate
- Unauthenticated / logged-out users are presented with a clean, minimal Sign-In screen displaying the Odyssey title/logo and a single **"Sign in with Google"** button.
- OAuth is configured with `prompt: 'select_account'` enabling effortless multi-account switching.
- Zero access to onboarding or dashboard without an active Supabase session.

### B. Persistent Profile Check & Skipping Repeated Onboarding
- On Google login or app startup:
  1. Checks user-scoped `localStorage` under `odyssey_profile_${user.id}` (with `lifeos_saved_profile` and legacy fallbacks).
  2. Queries Supabase `profiles` table (`.select('*').eq('id', user.id).single()`).
- **If existing profile / campaigns exist**:
  - Immediately hydrates Hero Name, Archetype, Current/Future Identity, Campaigns, Quests, XP Stats, Perks Wallet, and Weekly Reflections.
  - Sets `isOnboarded: true` and jumps straight to the Dashboard (`HomePage`), completely bypassing the onboarding flow.
- **If first-time user ever** (no record exists):
  - Pre-fills Google display name and avatar into the 3-step setup ("Begin Your Journey") shown only once.

### C. Safe Logout vs. Full System Format
- **Safe Sign Out (`🚪 Sign Out`)**:
  - Calls `supabaseClient.auth.signOut()` and clears only temporary auth tokens.
  - User profile, campaigns, quests, and XP remain preserved in localStorage and database.
- **Full System Format (`🚨 Full System Format`)**:
  - Prompts with in-app confirmation modal.
  - Wipes database record in Supabase (`onboarding_completed: false`, empty arrays).
  - Deletes all user keys from `localStorage`.
  - Signs out and restarts the app on the Google Sign-In screen; subsequent login prompts fresh setup.

---

## 👤 3. Identity Evolution & Gamification System

### A. Identity Mapping
- Core concept: Translating daily discipline into identity shifts (**Current Identity ➔ Future Identity Target**), e.g., *Student ➔ Product Designer*.
- **Persona Archetypes**:
  - `👤 Minimal Human`
  - `🎨 Creative Designer`
  - `🧭 Explorer`
  - `🛠️ Builder`
  - `📈 Entrepreneur`
  - `🤖 AI Creator`

### B. XP Economy & Dynamic Rank Tiers
- **Quest XP Values**: Small (+10 XP), Medium (+30 XP), Large (+100 XP).
- **Ranking System**:
  - Novice (Lvl 1–3) ➔ Scholar (Lvl 4–6) ➔ Builder (Lvl 7–9) ➔ Strategist (Lvl 10–12) ➔ Architect (Lvl 13–15) ➔ Creator (Lvl 16–18) ➔ Master (Lvl 19–21) ➔ Sage (Lvl 22+).
  - Dynamic avatar rings with animated level indicators.

### C. In-App Profile & Identity Editor (`✏️ Edit Profile`)
- Accessible from both the Hero profile card and the System Settings bar.
- Allows editing Hero Display Name, Avatar Archetype, Current Identity, and Future Identity target with real-time persistence.

---

## 🎯 4. Campaigns & Roadmap Management

### A. Custom Duration Units
- Flexible campaign length configuration during onboarding and within the Goals tab:
  - **Hours**, **Days**, **Weeks**, **Months**, **Years** (e.g., *30 Days*, *6 Months*, *1 Year*).
- Duration-based milestone progress algorithm preventing unrealistic 100% completion during initial weeks.

### B. Inline Campaign Editing (`✏️ Edit Campaign`)
- Users can edit any created campaign directly in the Roadmap / Goals view:
  - Update Campaign Name, Duration, Monthly Milestones, and Weekly Commitment Hours without page refreshes.

---

## ⚔️ 5. Quests & Task Cadence

### A. Quest Goal Cadence Badges
- Prominently displays `[Daily Goal]` or `[Weekly Goal]` tags across:
  - Main Dashboard feed
  - Quests Board
  - Campaign Roadmap

### B. Safe Deletion & 5-Second Undo Toast
- Trash bin icon (`🗑️`) replaces ambiguous delete buttons.
- Clicking delete prompts an In-App `<ConfirmDialog />` modal.
- Confirming triggers deletion and launches a 5-second interactive **[Undo]** toast at the bottom to restore the quest if needed.

### C. PWA Recurring Task Reset
- Built-in recurring task manager (`checkRecurringTasks`) automatically resets completed Daily and Weekly recurring quests for new cycles.

---

## 📝 6. Weekly Reflection & Inventory Archive

- **Intrinsic Reflection Flow**:
  - Guided prompt: Accomplishments, Obstacles/Friction Points, and Next Week's Strategy.
  - XP rewards removed from review submissions to maintain genuine introspection.
- **Collapsible Reviews Archive**:
  - Past reflections stored in an accordion stack grouped by week/date.
  - Expandable logs displaying Accomplished, Obstacles, and Strategy breakdown with individual log deletion support.

---

## 🎁 7. Perks & Rewards Wallet

- **XP Store & Perk Redemptions**:
  - Preset and custom perks with XP pricing (Daily 50 XP, Weekly 150 XP, Monthly 500 XP).
  - Categories: Entertainment, Food, Experiences, Creative, Shopping.
- **Theme-Adaptive Ticket Contrast**:
  - High-contrast ticket cards adapting dynamically to Light and Dark modes.

---

## 🛡️ 8. In-App Modal System (`<ConfirmDialog />`)

- Replaced all browser-native popup dialogs (`window.confirm()`, `window.alert()`) with a custom `<ConfirmDialog />` component.
- Features:
  - Translucent dark backdrop with `backdrop-filter: blur(10px)`.
  - Scale-in entry animation (`modalScaleIn`).
  - Dismissible on backdrop click or `[ Cancel ]`.
  - Red accent destructive styling (`[ Delete ]`, `[ Format & Restart ]`).

---

## 🏗️ 9. Architecture & Deployment Matrix

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend Framework** | React 18 (CDN) + Babel | Zero-build standalone Single Page Application |
| **Styling** | Vanilla CSS (CSS Variables) | Dark/Light mode theme system & iOS design tokens |
| **Database & Auth** | Supabase JS Client v2 | Google OAuth + `profiles` table JSON schema |
| **Local Storage** | Keyed LocalStorage (`odyssey_profile_*`) | Offline-first continuous data caching |
| **Static Deployment** | Vercel (`vercel.json`) | Root routing rewrites + `no-cache` cache headers |
| **Streamlit Cloud** | Python (`lifeos_app.py`, `streamlit_app.py`) | Single-file iframe embedding with Base64 PWA manifest |
