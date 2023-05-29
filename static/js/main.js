
//SPA
// Init state - the first loaded page
history.replaceState({ spaUrl: location.pathname }, "", location.pathname);

// Highlight menu-link
toggleActiveLink(location.pathname)

async function spa(spaUrl, doPushState = true) {
  const conn = await fetch(spaUrl, {
    method: "GET",
    headers: { spa: true },
  });

  // Get HTML
  let html
  try {
    html = await conn.text();
  }
  catch {
    console.warn("An error occured")
    return
  }

  // Remove old data
  document.querySelector("main").innerHTML = "";
  window.scrollTo(0,0)
  document.querySelector("main").insertAdjacentHTML("afterbegin", html);

  // Get and set title
  const title = document.querySelector(`[data-page_url="${spaUrl}"]`).dataset.page_title;
  document.querySelector("title").textContent = title;

  // Push state
  if (doPushState) {
    history.pushState({ spaUrl: spaUrl }, "", spaUrl);
  }

  // Set active class on site menu item
  toggleActiveLink(spaUrl);
  // Start infinite loader listener
  startInfiniteListener()
}

// History back/forth
window.addEventListener("popstate", (e) => {
  spa(e.state.spaUrl, false);
});

// ##############################
// ##############################
// ##############################

// Infinite scroll
let isLoading = false;

// Start infinite loader listener
startInfiniteListener()

function startInfiniteListener() {
  window.removeEventListener("scroll", determineLoad) // rm old
  if (!document.querySelector("#loader")) return; // set none if no loader
  window.addEventListener("scroll", determineLoad) // set new
  determineLoad() // init call (for if content is above the fold)
}

function determineLoad() {
  const loader = document.querySelector("#loader");
  if (loader.dataset.all_loaded) {
    window.removeEventListener("scroll", determineLoad)
    return
  }
  const loaderY = loader.getBoundingClientRect().y;
  if (loaderY < window.innerHeight && !isLoading) {
    isLoading = true
    fetchChunck(location.pathname, loader.dataset.offset);
  }
}

async function fetchChunck(endpoint, offset) {
  const loader = document.querySelector("#loader")
  loader.classList.remove("hide")

  const lastElm = loader.previousElementSibling
  const currentTopic = lastElm.dataset.topic
  let url = `${endpoint}?offset=${offset}`
  if (currentTopic) url += `&current-topic=${currentTopic}`
  
  const conn = await fetch(url, {
    headers: {as_chunk: true}
  })

  if (!conn.ok) {
    console.warn("Could not fetch chunk")
    return
  }

  // No content = all is loaded
  if (conn.status == 204) {
    window.removeEventListener("scroll", determineLoad)
    loader.dataset.all_loaded = true
    isLoading = false
    return
  }

  const html = await conn.text()
  loader.dataset.offset = Number(offset) + 50
  loader.insertAdjacentHTML("beforebegin", html)
  loader.classList.add("hide")


  isLoading = false
}

// ##############################
// ##############################
// ##############################

// CMS functionalities

function toggleTopSubMenu() {
  const target = event.target;
  const caret = target.querySelector(`.fa-caret-down`);
  const subMenu = document.querySelector(target.dataset.target);
  target.classList.toggle("text-secondary")
  caret.classList.toggle("rotate");

  const childElems = subMenu.querySelectorAll(`li`);
  if (subMenu.getAttribute("style")) {
    subMenu.removeAttribute("style");
  } else {
    subMenu.style.maxHeight = `${childElems.length * 50}px`;
  }
  
}

function toggleSideMenu() {
  const open = document.querySelector("#burger_open");
  const close = document.querySelector("#burger_close")
  const sideMenu = document.querySelector("#side_menu");
  open.classList.toggle("opacity-0");
  open.classList.toggle("rotate");
  close.classList.toggle("opacity-0");
  close.classList.toggle("rotate");
  sideMenu.classList.toggle("-translate-x-full");
}

function toggleActiveLink(path) {
  const href = `/${path.split("/")[1]}`
  const activeElm = document.querySelector(".side-menu-link.active");
  if ( activeElm ) activeElm.classList.remove("active");
  const newActiveElm = document.querySelector(`.side-menu-link[href="${href}"]`);
  if ( newActiveElm ) newActiveElm.classList.add("active")
}

function displayPreviewImage() {
  const input = (event.target);
  const image = input.files[0];
  const preview = document.querySelector(".image-preview");
  preview.querySelector("img").src = URL.createObjectURL(image);
  preview.classList.remove("hidden");
}

function removePreviewImage() {
  const inputId = event.target.dataset.inputId;
  document.querySelector(".image-preview").classList.add("hidden");
  document.querySelector(".image-preview img").src = "";
  document.querySelector(inputId).value = "";
  const inputHidden = document.querySelector(`[type='hidden'][data-input-id='${inputId}']`)
  if (inputHidden) {
      inputHidden.value = "";
  }
}

function toggleDeleteModal() {
  document.querySelector("body").classList.toggle("overflow-y-hidden");
  document.querySelector("#delete_modal").classList.toggle("hidden");
  document.querySelector(".action-bar-sub-menu").classList.add("hidden");
}

function toggleActionBarSubMenu() {
  document.querySelector(".action-bar-sub-menu").classList.toggle("hidden");
}

// ##############################
// ##############################
// ##############################

// API actions

function validateForm(callback) {
  event.preventDefault()
  const form = event.target.form
  let path = "";
  if (event.target.dataset.path) path = event.target.dataset.path;
  const isValid = form.checkValidity()
  if (!isValid) return
  callback(form, path);
}

async function postItem(form, path) {
  const conn = await fetch(`/api/v1/${path}`, {
    method: "POST",
    body: new FormData(form)
  });

  if (!conn.ok) {
    const error = await conn.json();
    console.log(error);
    return;
  }

  const id = await conn.json();
  spa(`/${path}/${id}`);
}

async function updateItem(form, path) {
  const id = getFormId(form, path);
  
  const conn = await fetch(`/api/v1/${path}/${id}`, {
    method: "PUT",
    body: new FormData(form)
  });

  if (conn.status === 204) return;
  const resp = await conn.json();
  handleResponseMessage(conn, resp);
}

async function deleteItem(form, path) {
  const id = form.id.value;

  const conn = await fetch(`/api/v1/${path}/${id}`, {
    method: "DELETE",
    body: new FormData(form)
  });

  if (!conn.ok) {
    const err = await conn.json();
    console.log(err);
    return;
  }

  // Success
  toggleDeleteModal();
  spa(`/${path}`);
}

async function postSearchItem() {
  const name = event.target.dataset.name;
  const key = event.target.dataset.key;
  const path = event.target.dataset.path;
  const target = event.target.dataset.target;
  const entryType = event.target.dataset.entry_type;

  if (name.length < 2 || name.length > 50) return;

  const form = new FormData();
  form.append(key, name);

  const conn = await fetch(`/api/v1/${path}`, {
    method: "POST",
    body: form
  });

  if (!conn.ok) {
    const err = await conn.json();
    console.log(err);
    return;
  }

  const id = await conn.json();
  selectSearchedItem(id, name, target, entryType);
}

async function updateUserPassword(form) {
  const conn = await fetch(`/api/v1/users/reset-password`, {
      method: "PUT",
      body: new FormData(form)
  })

  if (conn.status != 200) {
    const err = await conn.json()
    console.log(err)
    return
  }

  const res = await conn.json();
  console.log(res)

}

async function deleteBarAccess() {
  event.preventDefault();
  const form = event.target.form
  const userId = form.user_id.value

  const conn = await fetch('/api/v1/bar-access', {
    method: "DELETE",
    body: new FormData(form)
  })

  if (!conn.ok) {
    return
  }

  const res = await conn.json();
  console.log(res)
  spa(`/users/${userId}`)
}

async function postBarAccess() {
  event.preventDefault();
  const form = event.target.form
  const userId = form.user_id.value

  const conn = await fetch('/api/v1/bar-access', {
    method: 'POST',
    body: new FormData(form)
  })

  if (!conn.ok) {
    return
  }

  const res = await conn.json()
  console.log(res)
  spa(`/users/${userId}`)
}

async function signIn(form) {
  const errElm = document.querySelector(".hint-error");
  errElm.classList.add("hidden");
  errElm.textContent = "";

  const conn = await fetch('/sign-in', {
    method: "POST",
    body: new FormData(form)
  }); 
  if (!conn.ok) {
    const err = await conn.json();
    form.user_password.value = "";
    errElm.textContent = err.info;
    errElm.classList.remove("hidden");
  } else {
    window.location.href = "/select-location";
  }
}

async function selectLocation(form) {
  const errElm = document.querySelector(".hint-error");
  errElm.classList.add("hidden");
  errElm.textContent = "";

  const conn = await fetch('/select-location', {
    method: "POST",
    body: new FormData(form)
  });
  if (!conn.ok) {
    const err = await conn.json();
    errElm.textContent = err.info;
    errElm.classList.remove("hidden");
  } else {
    window.location.href = "/";
  }
}

async function searchBrewery() {
  const breweryName = event.target.form.brewery_name.value;
  const path = "breweries";
  const searchList = document.querySelector("#brewery_search");

  searchItem(breweryName, path, searchList);
}

async function searchBeerStyle() {
  const beerStyleName = event.target.form.beer_style_name.value;
  const path = "beer-styles";
  const searchList = document.querySelector("#beer_styles_search");

  searchItem(beerStyleName, path, searchList);
}

async function searchItem(name, path, searchList) {
  if (name.length < 2) {
    searchList.textContent = "";
    searchList.classList.add("hidden");
    return;
  }

  searchList.classList.remove("hidden");

  const conn = await fetch(`/api/v1/${path}/${name}?offset=0&limit=5`, {
    method: "GET",
    headers: {as_html: true}
  });
  
  if (!conn.ok) {
    const error = await conn.json()
    console.log(error);
    return;
  }

  const html = await conn.text();
  searchList.innerHTML = html;
}

async function searchBeers(){
  const form = event.target.form
  const beerName = form.beer_name.value
  const searchList = form.querySelector(".search-list")

  if (beerName.length < 2) {
    searchList.textContent = ""
    searchList.classList.add("hidden")
    return
  }

  searchList.classList.remove("hidden")

  const conn = await fetch(`/api/v1/beers?name=${beerName}`, {
    headers: {as_html : true}
  })

  if (conn.status != 200) return

  const html = await conn.text()
  console.log("html")
  searchList.innerHTML = html
}

async function selectSearchedBeer() {
  const elm = event.target;
  document.querySelector('#beer-name').value = elm.dataset.beer_name
  document.querySelector('#beer-id').value = elm.dataset.beer_id

  const infoHtml = `
  <div class="text-sm leading-none">
      <p>${elm.dataset.beer_style}</p>
      <p class="mt-1">${elm.dataset.brewery_name}</p>
      <div class="self-end text-xs flex justify-between max-w-[12rem] mt-1">
        <p>ALC.: ${elm.dataset.beer_alc}%</p>
        <span>|</span>
        <p>IBU: ${elm.dataset.beer_ibu}</p>
        <span>|</span>
        <p>EBC: ${elm.dataset.beer_ebc}</p>
    </div>
  </div>
  `
  document.querySelector(".beer-info").innerHTML = infoHtml

  elm.parentElement.parentElement.classList.add("hidden");
}

function selectSearchedItem(id=0, name="", target="", entryType="") {
  if (!id && !name && !target && !entryType) {
    id = event.target.dataset.id;
    name = event.target.dataset.name;
    target = event.target.dataset.target;
    entryType = event.target.dataset.entry_type;
  }
  document.querySelector(`#${entryType}_id`).value = id;
  document.querySelector(`#${entryType}_name`).value = name;
  document.querySelector(target).classList.add("hidden");
}


// ##############################

async function searchContentList() {
  const searchQuery = event.target.value
  if (searchQuery.length < 2) {
    hideSearchContent()
    return
  }
  const conn = await fetch(`${location.pathname}?name=${searchQuery}&limit=25`, {
    headers: {as_chunk: true}
  })
  if (!conn.ok) {
    hideSearchContent()
    return
  }

  if (conn.status == 204) {
    return showSearchContent("No results..")
  }

  const html = await conn.text()
  showSearchContent(html)
}

function hideSearchContent() {
  const searchContainer = document.querySelector(".content-search-container")
  searchContainer.classList.add("!hidden")
  searchContainer.innerHTML = ""
  document.querySelector(".content-container").classList.remove("!hidden")
  window.scrollTo(0,0)
}
function showSearchContent(html) {
  const searchContainer = document.querySelector(".content-search-container")
  searchContainer.classList.remove("!hidden")
  searchContainer.innerHTML = html
  document.querySelector(".content-container").classList.add("!hidden")
  window.scrollTo(0,0)
}

// ##############################
// ##############################
// ##############################

// Helper functions

function getFormId(form, path) {
  let id;
  switch(path) {
    case "beers":
      id = form.beer_id.value;
      break;
    case "beer-styles":
      id = form.beer_style_id.value;
      break;
    case "breweries":
      id = form.brewery_id.value;
      break;
    case "taps":
      id = form.tap_id.value;
      break;
    case "bars":
      id = form.bar_id.value;
      break;
    case "users":
      id = form.user_id.value;
      break; 
  }
  return id;
}

function handleResponseMessage(conn, resp) {
  const messElm = document.querySelector(".message");
  messElm.textContent = resp.info;

  if (!conn.ok) {
    messElm.classList.remove("success");
    messElm.classList.add("error");
  } else {
    if (resp.name) document.querySelector("h1").textContent = resp.name;
    messElm.classList.remove("error");
    messElm.classList.add("success");
  }
  messElm.classList.remove("hidden");
  window.scrollTo(0,0);
}