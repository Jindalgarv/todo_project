document.getElementById("register-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/api/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
        alert("Registration successful! You can now log in.");
        window.location.href = "/login/";
    } else {
        alert("Registration failed. Please try again.");
    }
});

document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/api/token/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem("accessToken", data.access);
        localStorage.setItem("refreshToken", data.refresh);
        window.location.href = "/todos/";
    } else {
        alert("Login failed. Please check your credentials.");
    }
});

document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
        window.location.href = "/login/";
        return;
    }

    const response = await fetch("/api/todos/", {
        headers: { Authorization: `Bearer ${token}` },
    });

    if (response.ok) {
        const todos = await response.json();
        const list = document.getElementById("todo-list");
        todos.forEach(todo => {
            const li = document.createElement("li");
            li.textContent = todo.title;
            list.appendChild(li);
        });
    } else {
        alert("Failed to load to-dos. Please log in again.");
        window.location.href = "/login/";
    }
});

document.getElementById("add-todo-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("accessToken");
    const title = document.getElementById("todo-title").value;

    const response = await fetch("/api/todos/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ title }),
    });

    if (response.ok) {
        window.location.reload();
    } else {
        alert("Failed to add to-do.");
    }
});


