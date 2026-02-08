import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';
import './Meeting.css';

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [step, setStep] = useState('setup'); // setup, meeting, result
  const [loading, setLoading] = useState(false);
  const [interviewId, setInterviewId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState("");
  const [sessionData, setSessionData] = useState({
    role_category: "Engineering & Tech",
    sub_role: "Full Stack Developer",
    difficulty_level: 1,
    target_company: "",
    job_description: "",
    is_panel: false,
    interviewer_name: "Adinath"
  });
  const [resumeFile, setResumeFile] = useState(null);
  const [evaluation, setEvaluation] = useState(null);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isMicOn, setIsMicOn] = useState(true);
  const [isCamOn, setIsCamOn] = useState(true);
  const [stream, setStream] = useState(null);
  const videoRef = useRef(null);
  const recognitionRef = useRef(null);

  // Initialize Speech Recognition once
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.lang = 'en-US';
      recognition.interimResults = true;
      recognition.continuous = true;

      recognition.onstart = () => setIsListening(true);
      recognition.onend = () => {
        if (step === 'meeting' && isMicOn) recognition.start(); // Auto-restart in meeting
      };

      recognition.onresult = (event) => {
        const transcript = Array.from(event.results)
          .map(result => result[0])
          .map(result => result.transcript)
          .join('');
        setUserInput(transcript);

        // Simulating "Interruption" logic or "Natural Stop" detection
        const lastResult = event.results[event.results.length - 1];
        if (lastResult.isFinal) {
          // You could auto-submit here if there's a long pause
          console.log("Final Transcript Segment:", lastResult[0].transcript);
        }
      };
      recognitionRef.current = recognition;
    }
  }, [step, isMicOn]);

  const toggleMic = () => {
    if (isMicOn) {
      recognitionRef.current?.stop();
    } else {
      recognitionRef.current?.start();
    }
    setIsMicOn(!isMicOn);
  };

  const toggleCam = () => {
    if (stream) {
      stream.getVideoTracks().forEach(track => track.enabled = !track.enabled);
    }
    setIsCamOn(!isCamOn);
  };

  const speak = (text) => {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);

    const voices = window.speechSynthesis.getVoices();
    const isFemale = sessionData.interviewer_name === "Veda";

    // Improved gender detection
    let voice = voices.find(v => {
      const name = v.name.toLowerCase();
      if (isFemale) {
        return (
          name.includes('female') ||
          name.includes('samantha') ||
          name.includes('zira') ||
          name.includes('vicki') ||
          name.includes('victoria') ||
          name.includes('google uk english female') ||
          name.includes('google us english') && v.lang.includes('en-US') // Fallback common high quality
        );
      }
      return (
        name.includes('male') ||
        name.includes('david') ||
        name.includes('mark') ||
        name.includes('google uk english male')
      );
    });

    utterance.voice = voice || voices[0];
    window.speechSynthesis.speak(utterance);
  };

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      setStream(mediaStream);
      if (videoRef.current) videoRef.current.srcObject = mediaStream;
    } catch (err) {
      console.error("Camera access denied", err);
    }
  };

  useEffect(() => {
    if (step === 'meeting') {
      startCamera();
      if (isMicOn) recognitionRef.current?.start();
    }
    return () => {
      stream?.getTracks().forEach(t => t.stop());
    };
  }, [step]);

  useEffect(() => {
    if (messages.length > 0 && messages[messages.length - 1].role === 'assistant') {
      speak(messages[messages.length - 1].content);
    }
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
        formData.append('is_panel', sessionData.is_panel);
        formData.append('job_description', sessionData.job_description);
        formData.append('interviewer_name', sessionData.interviewer_name);
        res = await axios.post(`${API_BASE}/interviews/upload-resume`, formData);
      } else {
        res = await axios.post(`${API_BASE}/interviews/start`, {
          ...sessionData,
          difficulty_level: parseInt(sessionData.difficulty_level)
        });
      }
      setInterviewId(res.data.id);
      setMessages([{ role: 'assistant', content: res.data.first_question }]);
      setStep('meeting');
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
    setLoading(false);
  };

  const submitAnswer = async () => {
    if (!userInput.trim()) return;
    const currentInput = userInput;
    setUserInput("");
    setMessages(prev => [...prev, { role: 'user', content: currentInput }]);
    setLoading(true);
    window.speechSynthesis.cancel();

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
    const roleCategories = [
      "Engineering & Tech", "Healthcare & Medical", "Business & Management",
      "Finance & Accounting", "Creative & Design", "Sales & Marketing",
      "Education & Training", "Legal", "Construction & Trades",
      "Hospitality & Tourism", "Social Services", "Science & Research"
    ];

    const interviewers = [
      { name: "Adinath", gender: "Male", v: "male", desc: "The Primal Sage. Strict, direct, and explores the depth of your foundations." },
      { name: "Veda", gender: "Female", v: "female", desc: "The Eternal Wisdom. Insightful, observant, and tests your clarity and vision." }
    ];

    return (
      <div className="setup-container">
        <header className="brand-header">
          <h1 className="gradient-text">InterviewAI</h1>
          <p>The Premium Simulation Room</p>
        </header>

        <div className="glass-card setup-box">
          <h2>Round Configuration</h2>

          <div className="interviewer-selector" style={{ marginBottom: '25px' }}>
            <label style={{ marginBottom: '10px', display: 'block' }}>Choose Your Interviewer</label>
            <div className="interviewer-grid" style={{ display: 'flex', gap: '15px' }}>
              {interviewers.map(int => (
                <div
                  key={int.name}
                  className={`interviewer-card glass-card ${sessionData.interviewer_name === int.name ? 'selected' : ''}`}
                  onClick={() => setSessionData({ ...sessionData, interviewer_name: int.name })}
                  style={{
                    flex: 1, padding: '15px', cursor: 'pointer', border: sessionData.interviewer_name === int.name ? '2px solid var(--primary)' : '1px solid var(--glass-border)',
                    background: sessionData.interviewer_name === int.name ? 'rgba(99, 102, 241, 0.1)' : 'transparent'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                    <span style={{ fontSize: '1.2rem' }}>{int.gender === "Male" ? "👨‍💼" : "👩‍💼"}</span>
                    <strong style={{ fontSize: '1.1rem' }}>{int.name}</strong>
                  </div>
                  <p style={{ fontSize: '0.8rem', opacity: 0.7, margin: 0 }}>{int.desc}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="input-row">
            <div className="input-group">
              <label>Role Category</label>
              <select
                value={sessionData.role_category}
                onChange={e => setSessionData({ ...sessionData, role_category: e.target.value })}
              >
                {roleCategories.map(r => <option key={r} value={r}>{r}</option>)}
              </select>
            </div>
            <div className="input-group">
              <label>Specific Sub-Role</label>
              <input
                type="text"
                placeholder="e.g. Senior Backend Dev"
                value={sessionData.sub_role}
                onChange={e => setSessionData({ ...sessionData, sub_role: e.target.value })}
              />
            </div>
          </div>

          <div className="input-row">
            <div className="input-group">
              <label>Target Company</label>
              <input
                type="text"
                placeholder="e.g. Google"
                value={sessionData.target_company}
                onChange={e => setSessionData({ ...sessionData, target_company: e.target.value })}
              />
            </div>
            <div className="input-group">
              <label>Difficulty</label>
              <select
                value={sessionData.difficulty_level}
                onChange={e => setSessionData({ ...sessionData, difficulty_level: parseInt(e.target.value) })}
              >
                <option value={1}>Junior (Level 1)</option>
                <option value={2}>Mid (Level 2)</option>
                <option value={3}>Senior (Level 3)</option>
              </select>
            </div>
          </div>

          <div className="checkbox-group" style={{ margin: '10px 0' }}>
            <input type="checkbox" id="panel" checked={sessionData.is_panel} onChange={e => setSessionData({ ...sessionData, is_panel: e.target.checked })} />
            <label htmlFor="panel">Enable Multi-Interviewer Panel (Elite Tier)</label>
          </div>

          <div className="input-group">
            <label>Upload Resume (PDF - Contextual AI Improvement)</label>
            <input type="file" accept=".pdf" onChange={e => setResumeFile(e.target.files[0])} />
          </div>

          <button className="primary-btn" onClick={startInterview} disabled={loading}>
            {loading ? "INITIALIZING SIMULATION..." : "ENTER MEETING ROOM"}
          </button>
        </div>
      </div>
    );
  }

  if (step === 'meeting') {
    return (
      <div className="meeting-container">
        <div className="status-overlay">
          <div className="live-dot"></div>
          <span>LIVE INTERVIEW: {sessionData.target_company || "General Technical"} Round</span>
        </div>

        <div className="meeting-main">
          <div className="interviewer-view glass-card">
            <div className="avatar-container">
              <div className="eye-pair">
                <div className="eye">
                  <div className="pupil" style={{
                    transform: isListening ? `translate(${(Math.random() - 0.5) * 10}px, ${(Math.random() - 0.5) * 10}px)` : 'translate(-50%, -50%)'
                  }}></div>
                </div>
                <div className="eye">
                  <div className="pupil" style={{
                    transform: isListening ? `translate(${(Math.random() - 0.5) * 10}px, ${(Math.random() - 0.5) * 10}px)` : 'translate(-50%, -50%)'
                  }}></div>
                </div>
              </div>
              <div className={`mouth ${isSpeaking ? 'speaking' : ''}`}></div>
              <p style={{ marginTop: '20px', color: 'rgba(255,255,255,0.6)', maxWidth: '80%', textAlign: 'center' }}>
                {messages[messages.length - 1].content}
              </p>
            </div>

            <div className="candidate-view">
              <video ref={videoRef} autoPlay playsInline muted />
              {!isCamOn && <div className="cam-off-overlay">Camera Off</div>}
            </div>
          </div>
        </div>

        <div className="meeting-toolbar">
          <button className={`tool-btn ${!isMicOn ? 'off' : ''}`} onClick={toggleMic}>
            {isMicOn ? '🎤' : '🎙️'}
          </button>
          <button className={`tool-btn ${!isCamOn ? 'off' : ''}`} onClick={toggleCam}>
            {isCamOn ? '📹' : '📸'}
          </button>
          <div className="tool-spacer" style={{ flex: 1 }}></div>

          <div className="voice-input-preview" style={{ color: 'white', fontSize: '0.8rem', opacity: 0.7 }}>
            {userInput || "AI is listening to your answer..."}
          </div>

          <button className="tool-btn primary" onClick={submitAnswer} disabled={loading}>
            {loading ? "EVALUATING..." : "SUBMIT RESPONSE"}
          </button>

          <button className="tool-btn off" onClick={() => window.location.reload()}>
            🛑 END
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
            {evaluation?.can_proceed ? "ROUND COMPLETE" : "INTERVIEW TERMINATED"}
          </h1>
          <div className="score-circle">
            <span className="score-num">{evaluation?.score}</span>
            <span className="total">/10</span>
          </div>
          <div className="feedback-section">
            <h3>Honest Recruiter Feedback:</h3>
            <p>{evaluation?.feedback}</p>
          </div>
          <button className="secondary-btn" onClick={() => window.location.reload()}>RE-ENTER SIMULATION</button>
        </div>
      </div>
    );
  }
}

export default App;
