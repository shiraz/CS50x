fetch('nav-bar.html')
.then(response => response.text())
.then(text => {
    const scriptElement = document.querySelector('#navbar');
    const navBar = document.createElement('nav');
    navBar.className = 'nav-bar';
    navBar.innerHTML = text;
    scriptElement.parentNode.replaceChild(navBar, scriptElement);
});