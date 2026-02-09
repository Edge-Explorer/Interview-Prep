import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Brain, Cpu, Shield, Zap, ArrowRight, MessageSquare, Award, BarChart3 } from 'lucide-react';

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
                    <div className="badge">NEW: Gemini 2.0 Flash Integration</div>
                    <h1>Master Your Next <br /> <span className="gradient-text">Big Opportunity</span></h1>
                    <p>
                        Experience the world's most realistic AI interview simulator.
                        Multi-round simulations, real-time vibe analysis, and professional feedback
                        tailored to your dream role.
                    </p>
                    <div className="hero-cta">
                        <button className="primary-btn-large" onClick={() => navigate('/signup')}>
                            Start Free Simulation <ArrowRight size={20} />
                        </button>
                        <div className="user-proof">
                            <div className="user-avatars">
                                <img src="https://i.pravatar.cc/150?u=1" alt="user" />
                                <img src="https://i.pravatar.cc/150?u=2" alt="user" />
                                <img src="https://i.pravatar.cc/150?u=3" alt="user" />
                            </div>
                            <span>Joined by 10,000+ candidates</span>
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
                            <span>Live Simulation: System Design Round</span>
                        </div>
                        <div className="card-body">
                            <div className="ai-message">"How would you handle a sudden 10x spike in traffic?"</div>
                            <div className="user-response">"I would implement horizontal scaling and..."</div>
                        </div>
                        <div className="card-footer">
                            <div className="stat"><span>Confidence:</span> 92%</div>
                            <div className="stat"><span>Technical Depth:</span> Excellent</div>
                        </div>
                    </div>
                    <div className="glow-sphere"></div>
                </motion.div>
            </header>

            {/* Features Section */}
            <section id="features" className="features">
                <h2>Built for <span className="gradient-text">High-Stakes</span> Success</h2>
                <div className="feature-grid">
                    <FeatureCard
                        icon={<Cpu />}
                        title="Reasoning Engine"
                        desc="Powered by Gemini 2.0 for deep technical follow-ups and realistic conversational flow."
                    />
                    <FeatureCard
                        icon={<Zap />}
                        title="Multi-Round Flow"
                        desc="Technical, Behavioral, System Design, and Managerial rounds. Just like a real onsite."
                    />
                    <FeatureCard
                        icon={<BarChart3 />}
                        title="Vibe Analysis"
                        desc="AI analyzes your tone, confidence, and facial expressions in real-time."
                    />
                    <FeatureCard
                        icon={<Shield />}
                        title="ATS Insights"
                        desc="Upload your resume and get direct feedback on how it aligns with your target role."
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
