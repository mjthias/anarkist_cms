
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
    headers: {"as-chunk": true}
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

// Start notofications if exist
if (document.querySelector("#notifications") && window.innerWidth > 600) {
  getNotifications()
  setInterval(getNotifications, 10000)
}
async function getNotifications() {
  const conn = await fetch("/api/v1/taps/notifications", {
    headers: {"as-html" : true}
  })

  if (!conn.ok) return

  const bellContainer = document.querySelector("#notifications")
  const subMenu = document.querySelector("#notifications-sub-menu")
  const ul = subMenu.querySelector("ul")

  if (conn.status == 204) {
    bellContainer.classList.add("hidden")
    subMenu.classList.add("hidden")
    ul.innerHTML = ""
    return
  }
  const html = await conn.text()
  ul.innerHTML = html
  const issues = ul.querySelectorAll("li").length
  const bellText = bellContainer.querySelector("p")
  bellText.textContent = issues
  bellContainer.classList.remove("hidden")
  subMenu.classList.remove("hidden")

}

// ##############################
// ##############################
// ##############################

// CMS functionalities

function toggleTopSubMenu() {
  const target = event.target;
  console.log(target)
  const caret = target.querySelector(`.fa-caret-down`);
  const subMenu = document.querySelector(target.dataset.target);
  target.classList.toggle("text-secondary")
  if (caret) caret.classList.toggle("rotate");


  const boxHeight = Number(subMenu.dataset.box_height)
  const liHeight = Number(subMenu.dataset.li_height)
  const childElems = subMenu.querySelectorAll(`li`).length;
  const height = boxHeight + liHeight * childElems
  console.log(childElems)
  if (subMenu.getAttribute("style")) {
    subMenu.removeAttribute("style");
  } else if (height > 400) {
    subMenu.style.maxHeight = "400px";
    subMenu.style.overflowY = "scroll"
  } else {
    subMenu.style.maxHeight = height + "px";
    subMenu.style.overflowY = "hidden"
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
  window.scrollTo(0,0);  
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
  let redir = "";
  if (event.target.dataset.path) path = event.target.dataset.path;
  if (event.target.dataset.redir) redir = event.target.dataset.redir;
  const isValid = form.checkValidity()
  if (!isValid) return
  callback(form, path, redir);
}

async function postItem(form, path) {
  const messElm = document.querySelector(".message");
  messElm.classList.add("hidden");
  messElm.classList.remove("success");
  messElm.classList.remove("error");
  messElm.innerHTML = "";

  const conn = await fetch(`/api/v1/${path}`, {
    method: "POST",
    body: new FormData(form)
  });

  if (!conn.ok) {
    const error = await conn.json();
    handleResponse(conn, error);
    return;
  }

  if (path == "bars") return window.location.href = "/"

  const resp = await conn.json();
  form.reset();

  if (path === "taps") {
    document.querySelector(".beer-info").innerHTML = "";
  }

  messElm.classList.remove("hidden");
  messElm.classList.add("success");
  messElm.innerHTML = `
    <span>
      ${resp.info} - 
      <a href="/${path}/${resp.id}" onclick="spa('/${path}/${resp.id}'); return false;">Go to ${resp.entry_type}</a>
    </span>
  `;
  window.scrollTo(0,0);
}

async function updateItem(form, path) {
  const id = getFormId(form, path);
  
  const conn = await fetch(`/api/v1/${path}/${id}`, {
    method: "PUT",
    body: new FormData(form)
  });

  if (!conn.ok) {
    const error = await conn.json();
    console.log(error)
    handleResponse(conn, error);
    return;
  }

  if (conn.status === 204) return;
  const resp = await conn.json();
  handleResponse(conn, resp);
}

async function deleteItem(form, path, redir) {
  const id = form.id.value;

  const conn = await fetch(`/api/v1/${path}/${id}`, {
    method: "DELETE",
    body: new FormData(form)
  });

  if (!conn.ok) {
    const err = await conn.json();
    handleResponse(conn, err);
    return;
  }

  // Success
  if (redir) return window.location.href = `/${redir}`
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

  const resp = await conn.json();
  selectSearchedItem(resp.id, name, target, entryType);
}

async function updateUserPassword(form) {
  const conn = await fetch(`/api/v1/users/reset-password`, {
      method: "PUT",
      body: new FormData(form)
  })
  console.logI()

  if (!conn.ok) {
    const err = await conn.json()
    handleResponse(conn, err)
    return
  }

  const res = await conn.json();
  handleResponse(conn, res)
}

async function deleteBarAccess() {
  const userId = event.target.dataset.user_id;
  const form = new FormData();
  form.append("user_id", userId);

  const conn = await fetch('/api/v1/bar-access', {
    method: "DELETE",
    body: form
  });

  if (!conn.ok) {
    const err = await conn.json();
    console.log(err);
    return;
  }

  spa(`/users/${userId}`);
}

async function postBarAccess() {
  const userId = event.target.dataset.user_id;
  const form = new FormData();
  form.append("user_id", userId);

  const conn = await fetch('/api/v1/bar-access', {
    method: "POST",
    body: form
  });

  if (!conn.ok) {
    const err = await conn.json();
    console.log(err);
    return;
  }

  spa(`/users/${userId}`);
}

async function deleteSignedInBar(form) {
  const id = form.id.value;
  const conn = await fetch(`/api/v1/bars/${id}`, {
    method: "DELETE",
    body: new FormData(form)
  });

  if (!conn.ok) {
    const err = await conn.json();
    handleResponse(conn, err);
    return;
  }

  // Success
  window.location.href = "/select-location"
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

async function selectLocation() {
  const barId = event.target.dataset.bar_id;
  const form = new FormData();
  const errElm = document.querySelector(".hint-error");
  
  errElm.classList.add("hidden");
  errElm.textContent = "";
  form.append("bar_id", barId);

  const conn = await fetch('/select-location', {
    method: "POST",
    body: form
  });

  if (!conn.ok) {
    const err = await conn.json();
    errElm.textContent = err.info;
    errElm.classList.remove("hidden");
    return;
  }
  window.location.href = "/";
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
    headers: {"as-html": true}
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
    headers: {"as-html" : true}
  })

  if (conn.status != 200) return

  const html = await conn.text()
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

async function changeLocation() {
  const barId = event.target.dataset.bar_id
  const form = new FormData()
  form.append("bar_id", barId)

  const conn = await fetch("/select-location", {
    method: "POST",
    body: form,
  })
  
  if (!conn.ok) return
  location.reload()
}


// ##############################

async function searchContentList() {
  const searchQuery = event.target.value
  if (searchQuery.length < 2) {
    hideSearchContent()
    return
  }
  const conn = await fetch(`${location.pathname}?name=${searchQuery}&limit=25`, {
    headers: {"as-chunk": true}
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

function handleResponse(conn, resp) {
  const messElm = document.querySelector(".message");
  messElm.classList.add("hidden");
  messElm.textContent = resp.info;

  if (!conn.ok) {
    try {
      const errElm = document.querySelector(`[name='${resp.key}']`);
      const errHint = document.querySelector(`[for='${resp.key}'] ~ .hint-error`);
      errHint.textContent = resp.info;
      errHint.classList.remove("hidden");
      errElm.classList.add("invalid");
      errElm.addEventListener("change", () => {
        errElm.classList.remove("invalid");
        errHint.classList.add("hidden");
        errHint.textContent = "";
      });
    } catch {
      messElm.classList.remove("success");
      messElm.classList.add("error");
      messElm.classList.remove("hidden");
    }
  } else {
    if (resp.name) document.querySelector("h1").textContent = resp.name;
    messElm.classList.remove("error");
    messElm.classList.add("success");
    messElm.classList.remove("hidden");
  }
  window.scrollTo(0,0);
}
