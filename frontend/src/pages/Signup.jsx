import React, {useState} from "react";
import axios from 'axios';
import { Link, useNavigate } from "react-router-dom";

const Signup = () =>{
    const [email,setEmail] = useState('');
    const [password,setPassword] = useState('');
    const [message,setMessage] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async(e)=>{
        e.preventDefault();
        try {
            const response = await axios.post('/api/signup',{email,password});
            if(response.data.message==="Successfully created"){
                navigate("/");
            } else {
                setMessage(response.data.message)
            }
        } catch (err) {
            setMessage('Signup Failed');
        }
    };
    return (
        <div className="d-flex justify-content-center align-items-center vh-100 bg-success">
            <div className="shadow-lg p-3 mb-5 bg-body-tertiary rounded bg-success-subtle">
                <div className="container">
                    <div className="container-fluid">
                        <main className="w-100 m-auto">
                            <form onSubmit={handleSubmit}>
                                <h1 className="h3 mb-3 fw-normal">Please sign up</h1>
                                <div className="form-floating m-3">
                                <input
                                    type="email"
                                    className="form-control"
                                    id="floatingInput"
                                    placeholder="name@example.com"
                                    value={email}
                                    onChange={(e)=>setEmail(e.target.value)}
                                    required
                                />
                                <label htmlFor="floatingInput">Email address</label>
                                </div>
                                <div className="form-floating m-3">
                                <input
                                    type="password"
                                    className="form-control"
                                    id="floatingPassword"
                                    placeholder="Password"
                                    value={password}
                                    onChange={(e)=>setPassword(e.target.value)}
                                    required
                                />
                                <label htmlFor="floatingPassword">Password</label>
                                </div>
                                <button className="btn btn-primary py-2 m-3" type="submit">
                                Sign up
                                </button>
                            </form>
                            <div className="row">
                                <div className="col-12">
                                    <p className="nav-item">Already have an account click <Link to="/">here</Link>  to Login</p>
                                </div>
                            </div>
                            {message && <p>{message}</p>}
                        </main>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Signup;