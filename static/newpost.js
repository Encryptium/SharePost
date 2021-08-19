const newpostBtn = document.getElementById("new-post");
const postsContainer = document.getElementById("posts");

newpostBtn.addEventListener('click', e => {
	postsContainer.innerHTML += 
	`<div class="post">
			<p class="title">[Title]</p>
			<p class="body">{Body Content}</p>
			<p class="timestamp"><i>{9:00 AM}</i></p>
		</div>`;
});