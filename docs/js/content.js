//written by Manuel Bieri, 2020

function head(icon) {
    document.write(
        '    <meta charset="UTF-8">\n' +
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n' +
        '    <meta http-equiv="X-UA-Compatible" content="IE=edge">\n' +
        '    <meta name="author" content="Manuel Bieri">\n' +
        '    <meta name="year" content="2020">\n\n' +
        '    <link rel="icon" href="icon/' + icon + '.ico" type="image/x-icon">'
    );
}

function navbar(active_item) {
    let active = {home: "", me: "", blog: "", forex: "", info: ""};
    active[active_item] = "active";
    document.write(
        '<div class="navbar">\n' +
        '    <a href="index.html" class="' + active["home"] + '"><img src="icon/home.png" alt="" class="nimg"> Home</a>\n' +
        '    <a href="me.html" class="' + active["me"] + '"><img src="icon/me.png" alt="" class="nimg"> Me</a>\n' +
        '    <a href="blog.html" class="' + active["blog"] + '"><img src="icon/blog.png" alt="" class="nimg"> Blog</a>\n' +
        '    <a href="forex.html" class="' + active["forex"] + '"><img src="icon/forex.png" alt="" class="nimg"> ForEx</a>\n' +
        '    <a href="info.html" class="' + active["info"] + '"><img src="icon/info.png" alt="" class="nimg"> Info</a>\n' +
        '</div>'
    );
}

function footer() {
    document.write(
        '<div class="footer">\n' +
        '    Hand-crafted by Manuel Bieri, 2020 (GPL V3)\n' +
        '</div>'
    );
}
