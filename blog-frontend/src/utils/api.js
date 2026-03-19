const API_URL = "https://web-production-a949.up.railway.app/";

export const registerUser = async (data) => {
    const res = await fetch(`${API_URL}/register`, {
        method: "POST",
        headers: {"Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    return res.json();
};

export const loginUser = async (data) => {
    const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    return res.json();
};

export const getPosts = async (data) => {
    const res = await fetch(`${API_URL}/posts`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
    return res.json();
};

export const createpost = async (token, data) => {
    const res = await fetch(`${API_URL}/posts`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
    bpdy: JSON.stringify(data),
    });
    return res.json();
};
