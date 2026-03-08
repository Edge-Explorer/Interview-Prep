import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate, Link } from 'react-router-dom';
import { Mail, Lock, ArrowRight, Brain } from 'lucide-react';
import { GoogleLogin } from '@react-oauth/google';
import axios from 'axios';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const res = await axios.post('http://localhost:8000/auth/login', { email, password });
            localStorage.setItem('token', res.data.access_token);
            localStorage.setItem('user', JSON.stringify(res.data.user));
            navigate('/dashboard');
        } catch (err) {
            alert(err.response?.data?.detail || "Login failed");
        }
        setLoading(false);
    };

    const handleGoogleSuccess = async (credentialResponse) => {
        try {
            const res = await axios.post('http://localhost:8000/auth/google', {
                token: credentialResponse.credential
            });
            localStorage.setItem('token', res.data.access_token);
            localStorage.setItem('user', JSON.stringify(res.data.user));
            navigate('/dashboard');
        } catch (err) {
            alert(err.response?.data?.detail || "Google Login failed");
        }
    };

    return (
        <div className="auth-container">
            <motion.div
                className="auth-box glass"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <div className="auth-header">
                    <Link to="/" className="auth-logo">
                        <Brain size={32} color="#6366f1" />
                        <span>InterviewAI</span>
                    </Link>
                    <h1>Welcome Back</h1>
                    <p>Continue your journey with a single click</p>
                </div>

                <div className="google-btn-container" style={{ margin: '40px 0' }}>
                    <GoogleLogin
                        onSuccess={handleGoogleSuccess}
                        onError={() => alert('Google Login Failed')}
                        useOneTap
                        theme="filled_black"
                        shape="pill"
                        size="large"
                    />
                </div>

                <div className="auth-footer">
                    Secure, one-tap authentication powered by Google.
                </div>
            </motion.div>
        </div>
    );
};

export default Login;
