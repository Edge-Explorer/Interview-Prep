import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Brain, Shield, Zap, ArrowRight, MessageSquare, Award } from 'lucide-react';

const LandingPage = () => {
    const navigate = useNavigate();

    return (
        <div className="landing-container">
            {/* Navbar */}
            <nav className="landing-nav">
                <div className="logo">
                    <Brain className="logo-icon" />
                    <span>InterviewAI</span>
                </div>
                <div className="nav-links">
                    <a href="#features">Features</a>
                    <button className="nav-login" onClick={() => navigate('/login')}>Login</button>
                    <button className="nav-signup" onClick={() => navigate('/signup')}>Get Started</button>
                </div>
            </nav>

            {/* Hero Section */}
            <header className="hero">
                <motion.div
                    className="hero-content"
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                >
                    <div className="badge">Built for Your First Big Break</div>
                    <h1>Crack Your First <br /> <span className="gradient-text">Dream Job</span></h1>
                    <p>
                        Build the confidence you need to ace your campus placements and entry-level interviews.
                        Practice with an AI that understands your journey—from academic projects to your first professional role.
                    </p>
                    <div className="hero-cta">
                        <button className="primary-btn-large" onClick={() => navigate('/signup')}>
                            Start Practice Session <ArrowRight size={20} />
                        </button>
                        <div className="user-proof">
                            <span>Helping freshers build confidence daily.</span>
                        </div>
                    </div>
                </motion.div>

                <motion.div
                    className="hero-visual"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 1, delay: 0.2 }}
                >
                    <div className="visual-card glass">
                        <div className="card-header">
                            <div className="pulse-dot"></div>
                            <span>Live Practice: Junior Developer Round</span>
                        </div>
                        <div className="card-body">
                            <div className="ai-message">"Can you explain the difference between a list and a tuple in simple terms?"</div>
                            <div className="user-response">"Sure! A list is mutable, which means I can change its elements, while a tuple is..."</div>
                        </div>
                        <div className="card-footer">
                            <div className="stat"><span>Confidence Score:</span> 88%</div>
                            <div className="stat"><span>Clarity:</span> Great!</div>
                        </div>
                    </div>
                    <div className="glow-sphere"></div>
                </motion.div>
            </header>

            {/* Features Section */}
            <section id="features" className="features">
                <h2>Your Path to <span className="gradient-text">Landing</span> That Job</h2>
                <div className="feature-grid">
                    <FeatureCard
                        icon={<Brain />}
                        title="Student-Smart AI"
                        desc="AI that knows exactly what freshers are asked—from basic DSA to core technical fundamentals."
                    />
                    <FeatureCard
                        icon={<Zap />}
                        title="Placement Readiness"
                        desc="Simulate the pressure of a real campus interview. Build the poise and clarity you need."
                    />
                    <FeatureCard
                        icon={<Award />}
                        title="Confidence Booster"
                        desc="Get real-time analysis of your speech and tone. Overcome the fear of speaking."
                    />
                    <FeatureCard
                        icon={<MessageSquare />}
                        title="Honest Feedback"
                        desc="No sugar-coating. Get the real feedback you need to fix your communication and logic gaps."
                    />
                </div>
            </section>

            {/* Footer */}
            <footer className="landing-footer">
                <div className="footer-content">
                    <div className="footer-brand">
                        <Brain size={32} />
                        <h2>InterviewAI</h2>
                    </div>
                    <p>© 2026 InterviewAI. All Rights Reserved.</p>
                </div>
            </footer>
        </div>
    );
};

const FeatureCard = ({ icon, title, desc }) => (
    <motion.div
        className="feature-card glass"
        whileHover={{ y: -10 }}
    >
        <div className="feature-icon">{icon}</div>
        <h3>{title}</h3>
        <p>{desc}</p>
    </motion.div>
);

export default LandingPage;
