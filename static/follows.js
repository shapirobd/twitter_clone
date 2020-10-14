// THIS IS A FAILED ATTEMPT AT A FURTHER STUDY TASK THAT I AM STILL WORKING ON

let $followForms = $(".form");

for (let index in $followForms) {
	let form = $followForms[index];
	let button = $(form).children()[0];
	$(form).on("submit", function (e) {
		e.preventDefault();
		console.log(form);
		handleFollowClick(form, button);
	});
}

async function handleFollowClick(form, button) {
	let $followed_user_id = $(button).attr("id");
	let newBtnHTML;

	if ($(form).hasClass("follow-form")) {
		let resp = await axios.post(`/users/follow/${$followed_user_id}`);
		$(form).removeClass("follow-form");
		$(form).addClass("unfollow-form");
		newBtnHTML = generateUnfollowButtonHTML($followed_user_id);
	} else if ($(form).hasClass("unfollow-form")) {
		let resp = await axios.post(`/users/stop-following/${$followed_user_id}`);
		$(form).removeClass("unfollow-form");
		$(form).addClass("follow-form");
		newBtnHTML = generateFollowButtonHTML($followed_user_id);
	}

	$(form).empty();
	$(form).append(newBtnHTML);
}

// async function createNewFollowButton(form, id, action, oldClass, newClass) {
// 	await axios.post(`/users/${action}/${id}`);
// 	$(form).removeClass(oldClass);
// 	$(form).addClass(newClass);
// 	return generateUnfollowButtonHTML($followed_user_id);
// }

function generateUnfollowButtonHTML(id) {
	return `<button class="btn btn-primary btn-sm" id="${id}">Unfollow</button>`;
}

function generateFollowButtonHTML(id) {
	return `<button class="btn btn-outline-primary btn-sm" id="${id}">Follow</button>`;
}
