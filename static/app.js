// THIS IS A FAILED ATTEMPT AT A FURTHER STUDY TASK THAT I AM STILL WORKING ON

let $followForms = $(".follow-form");
console.log($followForms);
for (let index in $followForms) {
	console.log(index);
	let form = $followForms[index];
	console.log(form);
	let button = $(form).children()[0];
	console.log(button);
	$(form).on("submit", async function (e) {
		e.preventDefault();

		let $followed_user_id = $(button).attr("id");
		console.log($followed_user_id);

		const resp = await axios.post(`/users/follow/${$followed_user_id}`);

		let followed_user = resp.data.followed_user;

		$(form).remove();
		console.log(followed_user);
		let newForm = generateFollowButtonFormHTML(followed_user);
		$(`#${followed_user.username}`).append(newForm);
	});
}

function generateFollowButtonFormHTML(followed_user) {
	`<form method="POST" action="/users/stop-following/${followed_user.id}" class="unfollow-form">
	    <button class="btn btn-primary btn-sm" id="${followed_user.id}">Unfollow</button>
	</form>`;
}
