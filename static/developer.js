function loadDeveloperConsole(type) {
	if (debug == "False") {
		console.log("Not allowed.");
		return;
	}

	if (type == "profile"){
		document.body.innerHTML += `<div id="dev-console"><p><b>Debug Info</b></p><p class="center">Username: "${debugInfo[0]}"</p><p class="center">Pfp: "${debugInfo[1]}"</p><p class="center">Developer: "${debugInfo[2]}"</p></div>`;
	}
	if (type == "post") {
		document.body.innerHTML += `<div id="dev-console"><p><b>Debug Info</b></p><p class="center">Post ID: <i>${debugInfo[0]}</i></p><p class="center">Username: <i>${debugInfo[1]}</i></p><p class="center">Arguments: <i>"${debugInfo[2]}"</i></p></div>`;
	}
}