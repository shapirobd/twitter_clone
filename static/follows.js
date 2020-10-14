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

function handleFollowClick(form, button) {
	let $followed_user_id = $(button).attr("id");
	let newBtnHTML;
	$(form).empty();
	if ($(form).hasClass("follow-form")) {
		createNewFollowButton(
			form,
			$followed_user_id,
			"follow",
			"follow-form",
			"unfollow-form"
		);
	} else if ($(form).hasClass("unfollow-form")) {
		createNewFollowButton(
			form,
			$followed_user_id,
			"stop-following",
			"unfollow-form",
			"follow-form"
		);
	}
}

async function createNewFollowButton(form, id, action, oldClass, newClass) {
	let resp = await axios.post(`/users/${action}/${id}`);
	$(form).removeClass(oldClass);
	$(form).addClass(newClass);
	if (action == "follow") {
		$(form).append(generateUnfollowButtonHTML(id));
	} else {
		$(form).append(generateFollowButtonHTML(id));
	}
}

function generateUnfollowButtonHTML(id) {
	return `<button class="btn btn-primary btn-sm" id="${id}">Unfollow</button>`;
}

function generateFollowButtonHTML(id) {
	return `<button class="btn btn-outline-primary btn-sm" id="${id}">Follow</button>`;
}
