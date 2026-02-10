# Frontend Pages - UI Flow

This directory contains the main page components that define the user journey from Landing to Interview Completion.

## 📂 Core Pages

### 1. `LandingPage.jsx`
The "Showcase" page. It uses heavy CSS animations and gradient typography to make a strong first impression. Features the platform's value proposition and CTAs.

### 2. `Login.jsx` & `Signup.jsx`
The Auth system. Clean, focused interfaces with validation logic and token management. They handle the interaction with the backend `/users/login` and `/users/signup` endpoints.

### 3. `Dashboard.jsx` (The Main App)
The most complex part of the frontend. It manages multiple "Steps":
- **`setup`**: User configuration (Interviewer, Role, Difficulty, Resume Upload).
- **`preparing`**: The "Analysis Screen" transition featuring the Live Resume Scanner.
- **`meeting`**: The real-time Interview Room with camera view, AI voice, and mic capture.
- **`result`**: The final Evaluation Screen showing scores and detailed AI feedback.

## 🎨 Professional Styling (`Auth.css`, `LandingPage.css`)
Separate CSS files are used to keep page-specific styling modular, while leveraging global CSS variables defined in `App.css`.

## ⚙️ Logic Managed:
- **State Management**: Handles user stats, session data, and message history.
- **Micro-animations**: Hover effects on cards, real-time mouth movement (AI talking), and progress bars.
