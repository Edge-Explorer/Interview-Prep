import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate, Link } from 'react-router-dom';
import { Mail, Lock, User, ArrowRight, Brain } from 'lucide-react';
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
                    <p>Prepare for your first big breakthrough</p>
                </div>

                <form onSubmit={handleSignup} className="auth-form">
                    <div className="auth-input-group">
                        <label>Full Name</label>
                        <div className="input-with-icon">
                            <User size={18} />
                            <input
                                type="text"
                                placeholder="John Doe"
                                value={formData.full_name}
                                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                                required
                            />
                        </div>
                    </div>

                    <div className="auth-input-group">
                        <label>Email Address</label>
                        <div className="input-with-icon">
                            <Mail size={18} />
                            <input
                                type="email"
                                placeholder="you@example.com"
                                value={formData.email}
                                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                required
                            />
                        </div>
                    </div>

                    <div className="auth-input-group">
                        <label>Password</label>
                        <div className="input-with-icon">
                            <Lock size={18} />
                            <input
                                type="password"
                                placeholder="Creating a strong password"
                                value={formData.password}
                                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                required
                            />
                        </div>
                    </div>

                    <button className="primary-btn-large" type="submit" disabled={loading}>
                        {loading ? "CREATING ACCOUNT..." : "SIGN UP"}
                        {!loading && <ArrowRight size={20} />}
                    </button>
                </form>

                <div className="auth-footer">
                    Already have an account? <Link to="/login">Log in here</Link>
                </div>
            </motion.div>
        </div>
    );
};

export default Signup;
