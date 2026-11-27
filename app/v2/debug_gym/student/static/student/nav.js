// [Student Dev] On narrow screens the student sidebar is a sideways strip: show the current page in it
const active = document.querySelector(".student-nav .is-active");
if (active && active.parentElement.scrollWidth > active.parentElement.clientWidth) {
  active.scrollIntoView({ block: "nearest", inline: "center" });
}
