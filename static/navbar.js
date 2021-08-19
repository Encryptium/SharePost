const navbar = document.getElementById("navbar");
const navContent = `<a title="Profile" href=\"/profile\"><img class=\"exclude-mobile\" id=\"logo-nav\" src=\"/static/images/profile/pfp-${pfp}.png\" alt=\"[PFP]\"><span id=\"name-corner\">${name.slice(1)}</span></a><ul><li><a href="/">Home</a></li><li><a href="/account">Account</a></li><li><a href="/newpost" title="New Post"><i class="fad fa-plus-square"  id="newpost-btn"></i></a></li></ul>`;

// <span id=\"new-post\">+</span>

navbar.innerHTML = navContent;