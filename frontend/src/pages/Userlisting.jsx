import React, { useEffect, useState, useContext } from "react";
import axios from "axios";
import { AuthContext } from "../context/AuthContext";

const Userlisting = () => {
    const { user, logout } = useContext(AuthContext);
    const [users, setUsers] = useState([]);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const token = user?.token;

                const response = await axios.get("/api/users", {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });

                setUsers(response.data);
            } catch (err) {
                setError("Failed to load users",err);
            } finally {
                setLoading(false);
            }
        };

        fetchUsers();
    }, [user]);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div className="container my-5">
            <h2>User List</h2>

            <button className="btn btn-danger mb-3" onClick={logout}>
                Logout
            </button>

            <ul className="list-group">
                {users.map((u) => (
                    <li key={u.id} className="list-group-item">
                        {u.email}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Userlisting;
