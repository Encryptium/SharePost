// c.execute(username TEXT, pwhash TEXT, bio TEXT, status TEXT, pfp 

function removeInvalidChars(name){
	var currInput = document.getElementsByName(name)[0].value;

  var newInput = currInput.replace(/[^A-Za-z0-9!\-~|]/g,'');

  document.getElementsByName(name)[0].value = newInput;
}