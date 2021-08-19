const profileTarget = document.querySelectorAll(".profile-img");

const profileIdentifier = document.querySelectorAll(".profile-img-id");

for (var i = 0; i < profileTarget.length; i++) {
	profileTarget[i].src = `/static/images/profile/pfp-${profileIdentifier[i].innerHTML}.png`;
}

// profileTarget.src = "/static/images/profile/loading.png";

// profileTarget.src = `/static/images/profile/pfp-${profileIndex}.png`;