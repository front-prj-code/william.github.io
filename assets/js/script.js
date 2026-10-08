'use strict';



// element toggle function
const elementToggleFunc = function (elem) { elem.classList.toggle("active"); }



// sidebar variables
const sidebar = document.querySelector("[data-sidebar]");
const sidebarBtn = document.querySelector("[data-sidebar-btn]");

// sidebar toggle functionality for mobile
sidebarBtn.addEventListener("click", function () { elementToggleFunc(sidebar); });



// testimonials variables
const testimonialsItem = document.querySelectorAll("[data-testimonials-item]");
const modalContainer = document.querySelector("[data-modal-container]");
const modalCloseBtn = document.querySelector("[data-modal-close-btn]");
const overlay = document.querySelector("[data-overlay]");

// modal variable
const modalImg = document.querySelector("[data-modal-img]");
const modalTitle = document.querySelector("[data-modal-title]");
const modalText = document.querySelector("[data-modal-text]");

// modal toggle function
const testimonialsModalFunc = function () {
  modalContainer.classList.toggle("active");
  overlay.classList.toggle("active");
}

// add click event to all modal items
for (let i = 0; i < testimonialsItem.length; i++) {

  testimonialsItem[i].addEventListener("click", function () {

    modalImg.src = this.querySelector("[data-testimonials-avatar]").src;
    modalImg.alt = this.querySelector("[data-testimonials-avatar]").alt;
    modalTitle.innerHTML = this.querySelector("[data-testimonials-title]").innerHTML;
    modalText.innerHTML = this.querySelector("[data-testimonials-text]").innerHTML;

    testimonialsModalFunc();

  });

}

// add click event to modal close button
modalCloseBtn.addEventListener("click", testimonialsModalFunc);
overlay.addEventListener("click", testimonialsModalFunc);



// custom select variables
const select = document.querySelector("[data-select]");
const selectItems = document.querySelectorAll("[data-select-item]");
const selectValue = document.querySelector("[data-selecct-value]");
const filterBtn = document.querySelectorAll("[data-filter-btn]");

select.addEventListener("click", function () { elementToggleFunc(this); });

// add event in all select items
for (let i = 0; i < selectItems.length; i++) {
  selectItems[i].addEventListener("click", function () {

    let selectedValue = this.innerText.toLowerCase();
    selectValue.innerText = this.innerText;
    elementToggleFunc(select);
    filterFunc(selectedValue);

  });
}

// filter variables
const filterItems = document.querySelectorAll("[data-filter-item]");

const filterFunc = function (selectedValue) {

  for (let i = 0; i < filterItems.length; i++) {

    if (selectedValue === "all") {
      filterItems[i].classList.add("active");
    } else if (selectedValue === filterItems[i].dataset.category) {
      filterItems[i].classList.add("active");
    } else {
      filterItems[i].classList.remove("active");
    }

  }

}

// add event in all filter button items for large screen
let lastClickedBtn = filterBtn[0];

for (let i = 0; i < filterBtn.length; i++) {

  filterBtn[i].addEventListener("click", function () {

    let selectedValue = this.innerText.toLowerCase();
    selectValue.innerText = this.innerText;
    filterFunc(selectedValue);

    lastClickedBtn.classList.remove("active");
    this.classList.add("active");
    lastClickedBtn = this;

  });

}



// contact form variables
const form = document.querySelector("[data-form]");
const formInputs = document.querySelectorAll("[data-form-input]");
const formBtn = document.querySelector("[data-form-btn]");

// add event to all form input field
for (let i = 0; i < formInputs.length; i++) {
  formInputs[i].addEventListener("input", function () {

    // check form validation
    if (form.checkValidity()) {
      formBtn.removeAttribute("disabled");
    } else {
      formBtn.setAttribute("disabled", "");
    }

  });
}



// page navigation variables
const navigationLinks = document.querySelectorAll("[data-nav-link]");
const pages = document.querySelectorAll("[data-page]");

// add event to all nav link
for (let i = 0; i < navigationLinks.length; i++) {
  navigationLinks[i].addEventListener("click", function () {

    for (let i = 0; i < pages.length; i++) {
      if (this.innerHTML.toLowerCase() === pages[i].dataset.page) {
        pages[i].classList.add("active");
        navigationLinks[i].classList.add("active");
        window.scrollTo(0, 0);
      } else {
        pages[i].classList.remove("active");
        navigationLinks[i].classList.remove("active");
      }
    }

  });
}



// project detail modal variables
const projectItems = document.querySelectorAll("[data-project-item]");
const projectModalContainer = document.querySelector("[data-project-modal-container]");
const projectModalOverlay = document.querySelector("[data-project-modal-overlay]");
const projectModalCloseBtn = document.querySelector("[data-project-modal-close]");

const projectModalImg = document.querySelector("[data-project-modal-img]");
const projectModalTitle = document.querySelector("[data-project-modal-title]");
const projectModalCategory = document.querySelector("[data-project-modal-category]");
const projectModalDesc = document.querySelector("[data-project-modal-desc]");
const projectModalActions = document.querySelector("[data-project-modal-actions]");

const toggleProjectModal = function () {
  if (projectModalContainer) {
    projectModalContainer.classList.toggle("active");
  }
};

if (projectItems.length > 0 && projectModalContainer) {
  for (let i = 0; i < projectItems.length; i++) {
    const trigger = projectItems[i].querySelector("[data-project-trigger]");
    if (!trigger) continue;

    trigger.addEventListener("click", function () {
      const payload = projectItems[i].querySelector(".project-modal-payload");
      if (!payload) return;

      const titleEl = payload.querySelector("[data-payload-title]");
      const catEl = payload.querySelector("[data-payload-category]");
      const imgEl = payload.querySelector("[data-payload-image]");
      const altEl = payload.querySelector("[data-payload-alt]");
      const descEl = payload.querySelector("[data-payload-desc]");

      const githubEl = payload.querySelector("[data-payload-github]");
      const webEl = payload.querySelector("[data-payload-web]");
      const npmEl = payload.querySelector("[data-payload-npm]");
      const linkEl = payload.querySelector("[data-payload-link]");

      if (projectModalImg) {
        projectModalImg.src = imgEl ? imgEl.innerText.trim() : "";
        projectModalImg.alt = altEl ? altEl.innerText.trim() : "";
      }
      if (projectModalTitle) projectModalTitle.innerText = titleEl ? titleEl.innerText.trim() : "";
      if (projectModalCategory) projectModalCategory.innerText = catEl ? catEl.innerText.trim() : "";
      if (projectModalDesc) projectModalDesc.innerText = descEl ? descEl.innerText.trim() : "";

      if (projectModalActions) {
        projectModalActions.innerHTML = "";

        if (webEl && webEl.dataset.payloadWeb) {
          const webBtn = document.createElement("a");
          webBtn.href = webEl.dataset.payloadWeb;
          webBtn.target = "_blank";
          webBtn.rel = "noopener noreferrer";
          webBtn.className = "project-modal-btn primary";
          webBtn.innerHTML = '<ion-icon name="globe-outline"></ion-icon><span>Live Demo / Web</span>';
          projectModalActions.appendChild(webBtn);
        }

        if (githubEl && githubEl.dataset.payloadGithub) {
          const ghBtn = document.createElement("a");
          ghBtn.href = githubEl.dataset.payloadGithub;
          ghBtn.target = "_blank";
          ghBtn.rel = "noopener noreferrer";
          ghBtn.className = "project-modal-btn secondary";
          ghBtn.innerHTML = '<ion-icon name="logo-github"></ion-icon><span>GitHub Repo</span>';
          projectModalActions.appendChild(ghBtn);
        }

        if (npmEl && npmEl.dataset.payloadNpm) {
          const npmBtn = document.createElement("a");
          npmBtn.href = npmEl.dataset.payloadNpm;
          npmBtn.target = "_blank";
          npmBtn.rel = "noopener noreferrer";
          npmBtn.className = "project-modal-btn secondary";
          npmBtn.innerHTML = '<ion-icon name="cube-outline"></ion-icon><span>NPM Package</span>';
          projectModalActions.appendChild(npmBtn);
        }

        if (!webEl && !githubEl && linkEl && linkEl.dataset.payloadLink) {
          const linkBtn = document.createElement("a");
          linkBtn.href = linkEl.dataset.payloadLink;
          linkBtn.target = "_blank";
          linkBtn.rel = "noopener noreferrer";
          linkBtn.className = "project-modal-btn primary";
          linkBtn.innerHTML = '<ion-icon name="open-outline"></ion-icon><span>View Project</span>';
          projectModalActions.appendChild(linkBtn);
        }
      }

      toggleProjectModal();
    });
  }

  if (projectModalCloseBtn) projectModalCloseBtn.addEventListener("click", toggleProjectModal);
  if (projectModalOverlay) projectModalOverlay.addEventListener("click", toggleProjectModal);

  window.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && projectModalContainer.classList.contains("active")) {
      toggleProjectModal();
    }
  });
}