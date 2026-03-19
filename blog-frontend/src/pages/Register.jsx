import { useState } from "react";
import { registerUser } from "../utils/api";

export default function Register() {
    const [form, setForm] = useState({
        
        username: "",
        password: "",
    });

    const handleSubmit = async (e) => {
        e.preventDefault();

        const res = await registerUser(form);
        console.log(res);

        alert("User registered! now login.");
    };

    return (
        <div>
            <h2>Register</h2>

            <form onsubmit={handleSubmit}>
                <input
                    placeholder="Username"
                    onChange={(e) =>
                        setForm({ ...form, username: e.target.value })
                    }
                />

                <input
                placeholder="Password"
                type="password"
                onChange={(e) =>
                    setForm({ ...form, password: e.target.value })
                }
                />
                <button type="submit">Register</button>
            </form>
        </div>
    );
}