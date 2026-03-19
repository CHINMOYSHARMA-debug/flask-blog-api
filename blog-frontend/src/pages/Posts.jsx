import { useEffect, useState } from "react";
import { getPosts, createPost } from "../utils/api";

export default function Posts() {
    const [posts, setPosts] = useState([])
    const [content, setcontent] = useState("")

    const token = localStorage.getItem("token")

    useEffect(() => {
        const fetchPosts = async () => {
            const res = await getPosts(token);
            console.log("POST RESPONSE:", res);

            const postsArray = res?.data?.posts || [];
            setPosts(postsArray);
        };

        fetchPosts();
    }, []);

    const handleCreate = async () => {
        await createPost(token, { content });
        
        const res = await getPosts(token);
        const postsArray = res?.data?.posts || [];
        setPosts(postsArray);

        setcontent("");
    };

    return (
        <div>
            <h2>Posts</h2>

            <input
                placeholder="WRITE SOMETHING"
                value = {content}
                onChange={(e) => setcontent(e.target.value)}
            />
            <button onClick={handleCreate}>/Create</button>

            <ul>
                {Array.isArray(posts) &&
                    posts?.map((p, i) => (
                        <li key={i}>{p.content}</li>
                    ))}
                </ul>
            </div>
        );
}
