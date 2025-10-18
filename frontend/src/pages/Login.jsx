import React, { useState } from "react";
import axios from "axios";
import "./Login.css";

function Login() {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "https://ativflow-backend.onrender.com/login",
        { email, senha }
      );
      if (response.data.token) {
        localStorage.setItem("token", response.data.token);
        window.location.href = "/dashboard";
      }
    } catch (error) {
      setErro("E-mail ou senha incorretos. Tente novamente.");
    }
  };

  return (
    <div className="login-container">
      <img src="/assets/logo.png" alt="Logo AtivFlow" className="login-logo" />
      <h1 className="login-title">AtivFlow</h1>

      <form onSubmit={handleLogin}>
        {erro && <p className="error-message">{erro}</p>}
        <input
          type="email"
          placeholder="E-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="login-input"
          required
        />
        <input
          type="password"
          placeholder="Senha"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
          className="login-input"
          required
        />
        <button type="submit" className="login-button">
          Entrar
        </button>
      </form>

      <div className="login-links">
        <p>
          <strong>Professora:</strong> maria.santos@senac.edu.br / Prof@123
        </p>
        <p>
          <strong>Aluno:</strong> samuel.ribeiro@adm321530.com / Aluno@123
        </p>
      </div>
    </div>
  );
}

export default Login;
