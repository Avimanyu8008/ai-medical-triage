import { useState, useEffect } from "react";
import { supabase } from "./lib/supabase";
import axios from "axios";

export default function App() {
  // 🔥 ENV (inside component)
  const API_BASE = import.meta.env.VITE_API_BASE;

  console.log("API BASE:", API_BASE);

  const AUDIO_API = `${API_BASE}/analyze`;
  const TEXT_API = `${API_BASE}/analyze-text`;

  const [session, setSession] = useState(null);

  const [audio, setAudio] = useState(null);
  const [text, setText] = useState("");

  const [detected, setDetected] = useState("");
  const [translated, setTranslated] = useState("");
  const [ai, setAi] = useState("");

  const [loading, setLoading] = useState(false);

  // ✅ AUTH STATE
  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => {
      setSession(data.session);
    });

    const { data: listener } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setSession(session);
      }
    );

    return () => {
      listener.subscription.unsubscribe();
    };
  }, []);

  // ✅ LOGIN
  const handleGoogleLogin = async () => {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
    });

    if (error) {
      console.error("Login error:", error.message);
    }
  };

  // ✅ LOGOUT
  const handleLogout = async () => {
    await supabase.auth.signOut();
  };

  const resetOutputs = () => {
    setDetected("");
    setTranslated("");
    setAi("");
  };

  // 🎤 AUDIO
  const handleAudio = async () => {
    if (!audio) {
      setAi("❌ Please upload audio file");
      return;
    }

    const formData = new FormData();
    formData.append("file", audio);

    setLoading(true);
    resetOutputs();

    try {
      const res = await axios.post(AUDIO_API, formData);

      setDetected(res.data.detected_text || "");
      setTranslated(res.data.translated_text || "");
      setAi(res.data.ai_response || "No AI response");
    } catch (err) {
      console.error(err);
      setAi("❌ Failed to connect to server");
    }

    setLoading(false);
  };

  // 🧾 TEXT
  const handleText = async () => {
    if (!text.trim()) {
      setAi("❌ Please enter symptoms");
      return;
    }

    setLoading(true);
    resetOutputs();

    try {
      const res = await axios.post(
        TEXT_API,
        new URLSearchParams({ text }),
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      setDetected(res.data.original_text || "");
      setTranslated(res.data.translated_text || "");
      setAi(res.data.ai_response || "No AI response");
    } catch (err) {
      console.error(err);
      setAi("❌ Failed to connect to server");
    }

    setLoading(false);
  };

  // 🔐 LOGIN SCREEN
  if (!session) {
    return (
      <div
        className="blackhole-bg"
        style={{ textAlign: "center", paddingTop: "150px" }}
      >
        <h1>🏥 AI Medical Triage</h1>

        <button onClick={handleGoogleLogin} style={styles.button}>
          Sign in with Google 🚀
        </button>
      </div>
    );
  }

  // ✅ MAIN APP
  return (
    <div className="blackhole-bg">
      <div style={styles.container}>
        <h1 style={styles.title}>🏥 AI Medical Triage</h1>

        {/* LOGOUT */}
        <div style={{ textAlign: "right", marginBottom: "10px" }}>
          <button onClick={handleLogout} style={styles.button}>
            Logout
          </button>
        </div>

        {/* AUDIO */}
        <div style={styles.card}>
          <h2>🎤 Voice Input</h2>
          <input
            type="file"
            accept="audio/*"
            onChange={(e) => setAudio(e.target.files[0])}
          />
          <button onClick={handleAudio} style={styles.button}>
            {loading ? "Analyzing..." : "Analyze Audio"}
          </button>
        </div>

        {/* TEXT */}
        <div style={styles.card}>
          <h2>🧾 Text Input</h2>
          <textarea
            style={styles.textarea}
            placeholder="Type symptoms (Tamil / Hindi / English)"
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <button onClick={handleText} style={styles.button}>
            {loading ? "Analyzing..." : "Analyze Text"}
          </button>
        </div>

        {/* RESULTS */}
        <div style={styles.card}>
          <h3>🧾 Results</h3>

          <div style={styles.label}>🎤 Detected</div>
          <div style={styles.resultBox}>{detected || "-"}</div>

          <div style={styles.label}>🌍 English</div>
          <div style={styles.resultBox}>{translated || "-"}</div>

          <div style={styles.label}>🧠 AI Advice</div>
          <div style={styles.resultBox}>
            <pre style={styles.pre}>{ai || "-"}</pre>
          </div>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "900px",
    margin: "auto",
    padding: "40px 20px",
    color: "white",
  },

  title: {
    textAlign: "center",
    fontSize: "2.5rem",
    marginBottom: "30px",
  },

  card: {
    background: "rgba(255,255,255,0.05)",
    backdropFilter: "blur(12px)",
    borderRadius: "16px",
    padding: "25px",
    marginBottom: "25px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.4)",
  },

  textarea: {
    width: "100%",
    height: "100px",
    marginTop: "10px",
    padding: "12px",
    borderRadius: "10px",
    border: "none",
    outline: "none",
  },

  button: {
    marginTop: "15px",
    padding: "12px 20px",
    background: "linear-gradient(135deg, #7c3aed, #9333ea)",
    color: "white",
    border: "none",
    borderRadius: "10px",
    cursor: "pointer",
  },

  resultBox: {
    background: "rgba(255,255,255,0.05)",
    padding: "12px",
    borderRadius: "10px",
    marginTop: "10px",
  },

  label: {
    fontWeight: "bold",
    marginTop: "15px",
  },

  pre: {
    whiteSpace: "pre-wrap",
  },
};