import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate, Link } from 'react-router-dom';
import { Mail, Lock, User, ArrowRight, Brain } from 'lucide-react';
import { GoogleLogin } from '@react-oauth/google';
import axios from 'axios';

const Signup = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        full_name: ''
    });
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSignup = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const res = await axios.post('http://localhost:8000/auth/signup', formData);
            localStorage.setItem('token', res.data.access_token);
            localStorage.setItem('user', JSON.stringify(res.data.user));
            navigate('/dashboard');
        } catch (err) {
            alert(err.response?.data?.detail || "Signup failed");
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
            alert(err.response?.data?.detail || "Google Signup failed");
        }
    };

    return (
        <div className="auth-container">
            <motion.div
                className="auth-box glass"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
            >
                <div className="auth-header">
                    <Link to="/" className="auth-logo">
                        <Brain size={32} color="#6366f1" />
                        <span>InterviewAI</span>
                    </Link>
                    <h1>Get Started</h1>
                    <p>Unlock your professional potential instantly</p>
                </div>

                <div className="google-btn-container" style={{ margin: '40px 0' }}>
                    <GoogleLogin
                        onSuccess={handleGoogleSuccess}
                        onError={() => alert('Google Signup Failed')}
                        useOneTap
                        theme="filled_black"
                        shape="pill"
                        text="signup_with"
                        size="large"
                    />
                </div>

                <div className="auth-footer">
                    Already have an account? Skip the form and <Link to="/login">Sign in here</Link>
                </div>
            </motion.div>
        </div>
    );
};

export default Signup;
