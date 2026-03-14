let currentEditId = null;

// LOGIN
async function login() {

const email = document.getElementById("email").value;
const password = document.getElementById("password").value;
const username = document.getElementById("username").value;

const res = await fetch("http://127.0.0.1:5000/login", {
method: "POST",
headers: {
"Content-Type": "application/json"
},
body: JSON.stringify({username, email, password})
});

const response = await res.json();

console.log("LOGIN RESPONSE:", response);

const token = response.data.access_token;

console.log("TOKEN FROM SERVER:", token);

if (!token) {
console.error("TOKEN MISSING");
return;
}

localStorage.setItem("token", token);
localStorage.setItem("user_id", response.data.user_id);

console.log("TOKEN SAVED:", localStorage.getItem("token"));

showMessage("Login successful");

}

// CREATE POST
async function createPost() {
    const btn = document.getElementById("create-btn");

    btn.disabled = true;
    btn.innerText = "Creating..";

    try {
        const title = document.getElementById("title").value;
        const content = document.getElementById("content").value;
        const token = localStorage.getItem("token");

        if (!token) {
            showMessage("Pleaselogin first", true);
            return;
        }
        
        console.log("TOKEN:", token);

        console.log("TOKEN BEING SENT:", token);
        const res = await fetch("http://127.0.0.1:5000/posts", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token   
            },
            body: JSON.stringify({ title, content })
        });
        const data = await res.json();
        showMessage(data.message);
        loadPosts();
    } catch (error) {
        showMessage("Error creating post", true);
    }
    finally {
        btn.disabled = false;
        btn.innerText = "Create";
    }
}

// LOAD POSTS
async function loadPosts() {
    try {
    const res = await fetch("http://127.0.0.1:5000/posts");
    const data = await res.json();

    console.log("POSTS:", data);

    const container = document.getElementById("posts");
    container.innerHTML = "";
    const posts = data.data.items;
    posts.forEach(post => {
        const postDiv = document.createElement("div");
        postDiv.classList.add("post");
        
        const currentUserId = Number(localStorage.getItem("user_id"));
        let buttons = "";

        if (post.author_id == currentUserId) {
            buttons = `
                <button onclick="editPost(${post.id})">Edit</button>
                <button onclick="deletePost(${post.id})">Delete</button>
            `;
        }
        
        postDiv.innerHTML = `
            <h3>${post.title}</h3>
            <p>${post.content}</p>
            ${buttons}
        `;
        container.appendChild(postDiv);
    });
} catch (error) {
    console.error("Error loading posts:", error);
    }
}

// EDIT POSTS
window.editPost = function(postId) {
    currentEditId = postId;

    const postDivs = document.querySelectorAll("#posts div");

    postDivs.forEach(div => {
        if (div.innerHTML.includes(`editPost(${postId})`)) {
            const title = div.querySelector("h3").innerText;
            const content = div.querySelector("p").innerText;

            document.getElementById("edit-title").value = title;
            document.getElementById("edit-content").value = content;
        }
    });

        document.getElementById("edit-section").style.display = "block";
};

// SUBMIT EDIT
async function submitEdit() {
    const title = document.getElementById("edit-title").value;
    const content = document.getElementById("edit-content").value;

    const token = localStorage.getItem("token");

    const res = await fetch(`http://127.0.0.1:5000/posts/${currentEditId}`, {
        method: "PUT",
        headers: {
            "Content-type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ title, content})
    });

    const data = await res.json();
    showMessage(data.message || data.msg);

    document.getElementById("edit-section").style.display = "none";

    loadPosts();
}

function showMessage(msg, isError = false) {
    const message = document.getElementById("message");
    
    message.innerText = msg;
    message.style.color = isError ? "red" : "green";

    setTimeout(() => {
        message.innerText = "";
    }, 3000);
}
 
// DELETE
window.deletePost = async function (postId) {
    const confirmDelete = confirm("Are you sure you want to Delete?");
    if(!confirmDelete) return;
    const token = localStorage.getItem("token")
    
    if (!token) {
        showMessage("Please login first", true);
        return;
    }
    
    try {
        const res = await fetch(`http://127.0.0.1:5000/posts/${postId}`, {
            method: "DELETE",
            headers: {
                "Authorization": "Bearer " + token
            }
        });
        const data = await res.json();

        if (!res.ok) {
            showMessage(data.message || "Delete failed", true);
            return;
        }

        showMessage(data.message);
        loadPosts();
    
    } catch(error) {
        console.error("DELETE ERROR:", error);
        showMessage("error deleting post", true);
    }
}
