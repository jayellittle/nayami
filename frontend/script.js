import { firebaseConfig } from './config.js';
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js';
import { getDatabase, ref, onValue, push } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-database.js';


// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getDatabase();
const postsRef = ref(db, 'posts');

// Listen for posts
onValue(postsRef, (snapshot) => {
    const posts = snapshot.val();
    displayPosts(posts);
});

// Display posts
function displayPosts(posts) {
    const postsDiv = document.getElementById('posts');
    postsDiv.innerHTML = '';
    
    if (posts) {
        Object.entries(posts).reverse().forEach(([key, post]) => {
            const postElement = document.createElement('div');
            postElement.className = 'post';
            const date = new Date(post.timestamp);
            postElement.innerHTML = `
                <div>${post.content}</div>
                <div class="timestamp">${date.toLocaleString()}</div>
            `;
            postsDiv.appendChild(postElement);
        });
    }
}

// Submit new post
window.submitPost = function() {
    const content = document.getElementById('content').value;
    if (content.trim()) {
        push(postsRef, {
            content: content,
            timestamp: Date.now()
        });
        document.getElementById('content').value = '';
    }
}
