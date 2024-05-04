const button_contact = document.querySelector('#submit');
const modal = document.getElementsByClassName("modal")[0];


button_contact.onclick = function ()  {
  modal.stylе.displаy = "block";
}
const closeModal = () => {
  modal.stylе.displаy = "none";
}