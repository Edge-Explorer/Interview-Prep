# Frontend Source - Components & Global Logic

This directory contains the main application components and global style definitions.

## 📂 Directories & Global Files

### `pages/`
Contains the top-level views/routes (Landing, Login, Dashboard, etc.).

### `assets/`
Static images and brand assets.

### Global Styles:
- **`App.css`**: The core style sheet. Contains all the complex animations (mesh-gradients, scanner-lines, pulse-effects) and the shared "Glass Card" system.
- **`Meeting.css`**: Specialized styles for the Interview Room (camera view, toolbar, speech bubbles).
- **`InterviewerCards.css`**: Styles for the premium 3D-selection cards in the dashboard.

## 🧠 Functional Details

### `App.jsx`
The main router of the application. It manages the public vs. private access and defines the layout wrappers.

### `main.jsx`
The application entry point that mounts the React app to the DOM and wraps it in strictly controlled state management.

### AI Interaction Layer
The frontend handles two major AI interactions:
1. **Speech-to-Text**: Using `window.webkitSpeechRecognition` to capture user answers.
2. **Text-to-Speech**: Using `window.speechSynthesis` with custom voice selection (Male/Adinath vs Female/Veda).
