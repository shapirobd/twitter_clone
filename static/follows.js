$(".form").each(function () {
	let button = $(this).children()[0];
	$(this).on("submit", function (e) {
		e.preventDefault();
		handleFollowClick(this, button);
	});
});

function handleFollowClick(form, button) {
	let $followed_user_id = $(button).attr("id");
	$(form).empty();
	if ($(form).hasClass("follow-form")) {
		renderNewFollowButton(
			form,
			$followed_user_id,
			"follow",
			"follow-form",
			"unfollow-form"
		);
	} else if ($(form).hasClass("unfollow-form")) {
		renderNewFollowButton(
			form,
			$followed_user_id,
			"stop-following",
			"unfollow-form",
			"follow-form"
		);
	}
}

// Should I make this two different functions with less parameters, or a single function with more parameters in order to avoid duplication?
async function renderNewFollowButton(form, id, action, oldClass, newClass) {
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
