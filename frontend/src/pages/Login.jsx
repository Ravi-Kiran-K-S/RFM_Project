import React, { useState, useContext } from "react";
import axios from 'axios';
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const navigate = useNavigate();
    const { login } = useContext(AuthContext);

    const handleSubmit = async (e) => {
    e.preventDefault();
    try {
        const response = await axios.post('/api/login', { email, password });

        const token = response.data.token;

        if (token) {
            login(token);  
            navigate("/users"); 
        } else {
            setMessage(response.data.message || "Login failed");
        }

    } catch (err) {
        setMessage("Login failed");
    }
};


    return (
        <div className="d-flex justify-content-center align-items-center vh-100 bg-info">
            <div className="shadow-lg p-3 mb-5 bg-body-tertiary rounded bg-info-subtle">
                <div className="container">
                    <main className="w-100 m-auto">
                        <form onSubmit={handleSubmit}>
                            <h1 className="h3 mb-3 fw-normal">Please sign in</h1>

                            <div className="form-floating m-3">
                                <input
                                    type="email"
                                    className="form-control"
                                    placeholder="name@example.com"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                />
                                <label>Email address</label>
                            </div>

                            <div className="form-floating m-3">
                                <input
                                    type="password"
                                    className="form-control"
                                    placeholder="Password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                />
                                <label>Password</label>
                            </div>

                            <button className="btn btn-primary py-2 m-3" type="submit">
                                Sign in
                            </button>
                        </form>

                        <p>Don't have an account? <Link to="/signup">Sign up</Link></p>

                        {message && <p>{message}</p>}
                    </main>
                </div>
            </div>
        </div>
    );
};

export default Login;
