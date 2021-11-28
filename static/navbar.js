const navbar = document.getElementById("navbar");

// Test if user session has PFP
try {
	var navContent = `<a title="Profile" href=\"/profile\"><span style="font-size: 31px"><img class=\"exclude-mobile\" id=\"logo-nav\" src=\"/static/images/profile/pfp-${pfp}.png\" alt=\"&#9676;\"></span><span id=\"name-corner\">${name.slice(1)}</span></a><ul><li><a href="/">Home</a></li><li><a href="/account">Account</a></li><li><a href="/draft" title="New"><img id=\"nav-newdraft\" src="/static/images/dft.png"></img></a></li></ul>`;
	console.log("Loading Navigation");
} catch(e) {
	console.log("PFP ELEMENT: NULL\nNavClear");
	var navContent = "";
}

navbar.innerHTML = navContent;

// Change image when hovering over draft btn
/*document.querySelector("#nav-newdraft").addEventListener('mouseover', e => {
	console.log("Boop!");
	document.querySelector("#nav-newdraft").src = "/static/images/draft.png";
});

document.querySelector("#nav-newdraft").addEventListener('mouseleave', e => {
	document.querySelector("#nav-newdraft").src = "/static/images/draft-bw.png";
});*/