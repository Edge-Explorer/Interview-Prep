# 🔐 Authentication & Security

This directory manages user security, password hashing, and token validation.

## 📂 Core Utility: `auth_utils.py`

Handles the heavy lifting for security using `passlib` (bcrypt) and `jose` (JWT).

### Key Features:
1. **Password Hashing**: Uses `bcrypt` for secure, industry-standard salted hashes.
2. **JWT Generation**: Creates transient access tokens for session management.
3. **Token Verification**: Decodes and validates incoming session tokens to protect API endpoints.
