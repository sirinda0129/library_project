var menuButton = document.querySelector(".burger-menu-btn");
var headerMenu = document.querySelector(".header__user-menu");

menuButton.addEventListener("click", function (evt) {
  evt.preventDefault();
  if (headerMenu.classList.contains("header__user-menu--opened")) {
    headerMenu.classList.remove("header__user-menu--opened");
    headerMenu.classList.add("header__user-menu--closed");
  } else if (headerMenu.classList.contains("header__user-menu--closed")) {
    headerMenu.classList.remove("header__user-menu--closed");
    headerMenu.classList.add("header__user-menu--opened");
  }
});