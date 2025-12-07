import React from "react";
import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Userlisting from "./pages/Userlisting";

function App(){
  return (
    <>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/users" element={<Userlisting />} />
        </Routes>
    </>
  );
}

export default App;