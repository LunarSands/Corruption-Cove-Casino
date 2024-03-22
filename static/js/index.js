function search(){
    var userToFind = document.getElementById('accountToFind').value;
    var url = slugify(userToFind);
    window.location.href = url;
}

function slugify(input) {
    var slug = "";
    var users = JSON.parse(users_safe);
    for (var user in users) {
        if (input === user) {
            slug = users[user];
            break;
        }
    }
    if (slug){
        return "/corruption-cove-casino/account/" + slug + "/";
    }
    else{
        return "/corruption-cove-casino/";
    }
}