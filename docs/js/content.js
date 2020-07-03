//written by Manuel Bieri, 2020

function head(icon) {
    document.write(
        '    <meta charset="UTF-8">\n' +
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n' +
        '    <meta http-equiv="X-UA-Compatible" content="IE=edge">\n' +
        '    <meta name="author" content="Manuel Bieri">\n' +
        '    <meta name="year" content="2020">\n\n'
        //'    <link rel="icon" href="icon/' + icon + '.ico" type="image/x-icon">' // no icons available at the moment
    );
}

function navbar(active_item) {
    let active = {Home: "", About: "", GitHub: ""};
    active[active_item] = "active";
    document.write(
        '<div class="navbar">\n' +
        '    <a href="index.html" class="' + active["Home"] + '"><img src="" alt="" class="nimg"> Home</a>\n' +
        '    <a href="about.html" class="' + active["About"] + '"><img src="" alt="" class="nimg"> About</a>\n' +
        '    <a href="github.html" class="' + active["GitHub"] + '"><img src="" alt="" class="nimg"> GitHub</a>\n' +
        '</div>'
    );
}

function footer() {
    document.write(
        '<div class="footer">\n' +
        '    Created by Manuel Bieri, 2020 (GPL V3)\n' +
        '</div>'
    );
}
