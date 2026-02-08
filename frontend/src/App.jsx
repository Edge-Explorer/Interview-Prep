import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE = "http://localhost:8000";

function App() {
  const [step, setStep] = useState('setup'); // setup, chat, result
  const [loading, setLoading] = useState(false);
  const [interviewId, setInterviewId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState("");
  const [sessionData, setSessionData] = useState({
    role_category: "SDE",
    sub_role: "Full Stack Developer",
    difficulty_level: 1,
    target_company: "",
    job_description: "",
    is_panel: false
  });
  const [resumeFile, setResumeFile] = useState(null);
  const [evaluation, setEvaluation] = useState(null);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const startInterview = async () => {
    setLoading(true);
    try {
      let res;
      if (resumeFile) {
        const formData = new FormData();
        formData.append('file', resumeFile);
        formData.append('role_category', sessionData.role_category);
        formData.append('sub_role', sessionData.sub_role);
        formData.append('difficulty_level', sessionData.difficulty_level);
        formData.append('target_company', sessionData.target_company);
        formData.append('job_description', sessionData.job_description);

        res = await axios.post(`${API_BASE}/interviews/upload-resume`, formData);
      } else {
        res = await axios.post(`${API_BASE}/interviews/start`, {
          ...sessionData,
          difficulty_level: parseInt(sessionData.difficulty_level)
        });
      }

      setInterviewId(res.data.id);
      setMessages([{ role: 'assistant', content: res.data.first_question }]);
      setStep('chat');
    } catch (err) {
      alert("Error starting interview. Is the backend running?");
    }
    setLoading(false);
  };

  const submitAnswer = async () => {
    if (!userInput.trim()) return;
    const currentInput = userInput;
    setUserInput("");
    setMessages(prev => [...prev, { role: 'user', content: currentInput }]);
    setLoading(true);

    try {
      const res = await axios.post(`${API_BASE}/interviews/submit-answer`, {
        interview_id: interviewId,
        answer: currentInput
      });

      setEvaluation(res.data.evaluation);

      if (res.data.terminated) {
        setStep('result');
      } else {
        setMessages(prev => [...prev, { role: 'assistant', content: res.data.next_question }]);
      }
    } catch (err) {
      alert("Submission failed.");
    }
    setLoading(false);
  };

  if (step === 'setup') {
    return (
      <div className="setup-container">
        <header className="brand-header">
          <h1 className="gradient-text">InterviewAI</h1>
          <p>The Honest Prep Platform</p>
        </header>

        <div className="glass-card setup-box">
          <h2>Configure Your Simulation</h2>

          <div className="input-group">
            <label>Field</label>
            <select value={sessionData.role_category} onChange={e => setSessionData({ ...sessionData, role_category: e.target.value })}>
              <option value="SDE">Software Engineering</option>
              <option value="Data Science">Data Science / ML</option>
              <option value="HR">Human Resources</option>
              <option value="Management">Management</option>
              <option value="Sales">Sales / Marketing</option>
            </select>
          </div>

          <div className="input-group">
            <label>Specific Role (e.g. SDE-2, ML Engineer)</label>
            <input type="text" placeholder="Full Stack Developer" value={sessionData.sub_role} onChange={e => setSessionData({ ...sessionData, sub_role: e.target.value })} />
          </div>

          <div className="input-group">
            <label>Target Company (Optional)</label>
            <input type="text" placeholder="Google, Amazon, etc." value={sessionData.target_company} onChange={e => setSessionData({ ...sessionData, target_company: e.target.value })} />
          </div>

          <div className="input-group">
            <label>Difficulty</label>
            <div className="difficulty-pills">
              {[1, 2, 3].map(level => (
                <button
                  key={level}
                  className={sessionData.difficulty_level === level ? "active" : ""}
                  onClick={() => setSessionData({ ...sessionData, difficulty_level: level })}
                >
                  {level === 1 ? 'Junior' : level === 2 ? 'Mid' : 'Senior'}
                </button>
              ))}
            </div>
          </div>

          <div className="checkbox-group">
            <input type="checkbox" checked={sessionData.is_panel} onChange={e => setSessionData({ ...sessionData, is_panel: e.target.checked })} />
            <label>Enable Multi-Interviewer Panel (Elite Master Tier)</label>
          </div>

          <div className="input-group">
            <label>Upload Resume (PDF - Optional for ATS Analysis)</label>
            <input type="file" accept=".pdf" onChange={e => setResumeFile(e.target.files[0])} />
          </div>

          <button className="primary-btn" onClick={startInterview} disabled={loading}>
            {loading ? "INITIALIZING AI..." : "START HONEST INTERVIEW"}
          </button>
          <p className="warning-text">⚠️ Warning: Feedback is honest and unsugarcoated.</p>
        </div>
      </div>
    );
  }

  if (step === 'chat') {
    return (
      <div className="chat-container">
        <div className="chat-header glass-card">
          <div className="status">LIVE SIMULATION: {sessionData.target_company || "Standard Round"}</div>
          <div className="role">{sessionData.sub_role}</div>
        </div>

        <div className="chat-window">
          {messages.map((m, i) => (
            <div key={i} className={`message-bubble ${m.role}`}>
              <div className="sender">{m.role === 'assistant' ? 'INTERVIEWER' : 'YOU'}</div>
              <div className="text">{m.content}</div>
            </div>
          ))}
          {loading && <div className="loading-dots">Interviewer is thinking<span>.</span><span>.</span><span>.</span></div>}
          <div ref={chatEndRef} />
        </div>

        <div className="chat-input-box glass-card">
          <textarea
            placeholder="Type your answer here... Be precise."
            value={userInput}
            onChange={e => setUserInput(e.target.value)}
            onKeyDown={e => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                submitAnswer();
              }
            }}
          />
          <button className="send-btn" onClick={submitAnswer} disabled={loading}>
            SUBMIT ANSWER
          </button>
        </div>
      </div>
    );
  }

  if (step === 'result') {
    return (
      <div className="result-container">
        <div className="glass-card result-box">
          <h1 className={evaluation?.can_proceed ? "success-text" : "fail-text"}>
            {evaluation?.can_proceed ? "ROUND PASSED!" : "INTERVIEW TERMINATED"}
          </h1>

          <div className="score-circle">
            <span className="score-num">{evaluation?.score}</span>
            <span className="total">/10</span>
          </div>

          <div className="feedback-section">
            <h3>Honest Feedback:</h3>
            <p>{evaluation?.feedback}</p>
          </div>

          {!evaluation?.can_proceed && (
            <div className="roadmap-teaser">
              <p>You failed the benchmark (7/10). Get a customized 7-day roadmap to fix your gaps.</p>
              <button className="premium-btn">UNLOCK ELITE ROADMAP (₹499)</button>
            </div>
          )}

          <button className="secondary-btn" onClick={() => window.location.reload()}>TRY AGAIN</button>
        </div>
      </div>
    );
  }
}

export default App;
