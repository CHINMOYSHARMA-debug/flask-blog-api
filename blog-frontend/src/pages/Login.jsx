import { useState } from  "react";
import { loginUser } from "../utils/api";

export default function Login() {
    const [form, setForm] = useState({
        username:"",
        password: "",
    });

    const handleSubmit = async (e) => {
        e.preventDefault();

        const res = await loginUser(form);
        console.log(res);

        if (res.success) {
            const token = res.data.access_token;

            localStorage.setItem("token", token);
            
            alert("Login Successful") 
        } else {
            alert(res.error || "Login failed");
        }
    };

    return (
        <div>
            <h2>Login</h2>
        <form onSubmit={handleSubmit}>
            <input
                placeholder="Username"
                onChange={(e) =>
                    setForm({ ...form, username: e.target.value})
                }
            />

            <input
                placeholder="Password"
                type="password"
                onChange={(e) =>
                    setForm({ ...form, password: e.target.value})
                }
            />

            <button type="submit">Login</button>
        </form>
    </div>
);

}
