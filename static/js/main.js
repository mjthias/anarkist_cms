
//SPA
// Init state - the first loaded page
history.replaceState({ spaUrl: location.pathname }, "", location.pathname);

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
}

// History back/forth
window.addEventListener("popstate", (e) => {
  spa(e.state.spaUrl, false);
});

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

function toggleActiveLink(elem) {
  document.querySelectorAll(".side-menu-link").forEach(link => {
    link.classList.remove("active");
  });
  document.querySelector(`.side-menu-link[href="${elem}"]`).classList.add("active");
  toggleSideMenu();
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

// ##############################
// ##############################
// ##############################

// API actions

function validateForm(callback) {
  event.preventDefault()
  const form = event.target.form
  const isValid = form.checkValidity()
  if (!isValid) return
  callback(form)
}


async function postUser(form) {
  const conn = await fetch("/api/v1/users", {
    method: "POST",
    body: new FormData(form)
  })

  if (!conn.ok) {
    const err = await conn.json()
    console.log(err)
    return
  }

  const userId = await conn.json()
  spa(`/users/${userId}`)
}


async function deleteUser(form) {
  const userId = form.user_id.value
  const conn = await fetch(`/api/v1/users/${userId}`, {
    method: 'DELETE',
    body: new FormData(form)
  })

  if (!conn.ok) {
    return
  }

  const res = await conn.json()
  console.log(res)
}


async function updateUserInfo(form) {
  const userId = form.user_id.value;
  const conn = await fetch(`/api/v1/users/${userId}`, {
    method: "PUT",
    body: new FormData(form)
  });

  if (conn.status != 200) {
    const err = await conn.json()
    console.log(err)
    return
  }

  const res = await conn.json()
  console.log(res)
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

async function signIn() {
  const form = event.target.form;
  // TODO: VALIDATE INPUT VALUES

  const connection = await fetch('/sign-in', {
    method: "POST",
    body: new FormData(form)
  }); 
  const response = await connection.json()
  if (!connection.ok) {
    // TODO: Display error message to user
  } else {
    window.location.href = "/select-location";
  }
}

async function selectLocation() {
  const form = event.target.form;
  // TODO: VALIDATE INPUT VALUES

  const connection = await fetch('/select-location', {
    method: "POST",
    body: new FormData(form)
  });
  const response = await connection.json();
  if (!connection.ok) {
    // TODO: Display error to user
  } else {
    window.location.href = "/";
  }
}

async function postBrewery(form) {
  const conn = await fetch("/api/v1/breweries", {
    method: "POST",
    body: new FormData(form)
  })

  if (!conn.ok) {
    const err = await conn.json()
    console.log(err)
    return
  }

  const breweryId = await conn.json()
  spa(`/breweries/${breweryId}`)
}

async function postSearchBrewery() {
  const breweryName = event.target.dataset.brewery_name;

  if (breweryName.length < 2 || breweryName.length > 50) return;

  const form = new FormData();
  form.append("brewery_name", breweryName);

  const conn = await fetch("/api/v1/breweries", {
    method: "POST",
    body: form
  });

  if (!conn.ok) {
    const err = await conn.json();
    console.log(err);
    return;
  }
  const breweryId = await conn.json();
  selectSearchedItem(breweryId, breweryName, "#brewery_search", "brewery");
}

async function updateBrewery(form) {
  const breweryId = form.brewery_id.value
  const conn = await fetch(`/api/v1/breweries/${breweryId}`, {
    method: "PUT",
    body: new FormData(form)
  })

  if (!conn.ok) {
    const error = await conn.json()
    console.log(error)
    // TODO handle error
  }

  // Success
}

async function deleteBrewery(form) {
  const breweryId = form.brewery_id.value
  const conn = await fetch(`/api/v1/breweries/${breweryId}`, {
    method: "DELETE",
    body: new FormData(form)
  })
  if (!conn.ok) {
    // TODO handle error
    const error = await conn.json()
    console.log(error)
    return
  }

  // SUCCES
  spa("/breweries")
}

async function searchBrewery() {
  const form = event.target.form;
  const breweryName = form.brewery_name.value;
  const searchList = document.querySelector("#brewery_search");

  if (breweryName.length < 2) {
    searchList.textContent = "";
    searchList.classList.add("hidden");
    return;
  }

  searchList.classList.remove("hidden");

  const conn = await fetch(`/api/v1/breweries/${breweryName}?offset=0&limit=5`, {
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

async function postBeerStyle(form) {
  const conn = await fetch('/api/v1/beer-styles', {
    method: "POST",
    body: new FormData(form)
  });

  if (!conn.ok) {
    const error = await conn.json();
    console.log(error);
    return;
  }

  const beerStyleId = await conn.json();
  spa(`/beer-styles/${beerStyleId}`);

}

async function postSearchBeerStyle() {
  const beerStyleName = event.target.dataset.beer_style_name;

  if (beerStyleName.length < 2 || beerStyleName.length > 50) return;

  const form = new FormData();
  form.append("beer_style_name", beerStyleName);

  const conn = await fetch("/api/v1/beer-styles", {
    method: "POST",
    body: form
  });

  if (!conn.ok) {
    const err = await conn.json();
    console.log(err);
    return;
  }
  const beerStyleId = await conn.json();
  selectSearchedItem(beerStyleId, beerStyleName, "#beer_styles_search", "beer_style");
}

async function updateBeerStyle(form) {
  const beerStyleId = form.beer_style_id.value;
  const conn = await fetch(`/api/v1/beer-styles/${beerStyleId}`, {
    method: "PUT",
    body: new FormData(form)
  });

  if (!conn.ok) {
    const error = await conn.json();
    console.log(error);
    return;
  }

  // SUCCESS
}

async function deleteBeerStyle(form) {
  const beerStyleId = form.id.value;
  const conn = await fetch(`/api/v1/beer-styles/${beerStyleId}`, {
    method: "DELETE",
    body: new FormData(form)
  });

  if (!conn.ok) {
    const error = await conn.json();
    console.log(error);
    return;
  }

  spa('/beer-styles')
}

async function searchBeerStyle() {
  const form = event.target.form;
  const beerStyleName = form.beer_style_name.value;
  const searchList = document.querySelector("#beer_styles_search");

  if (beerStyleName.length < 2) {
    searchList.textContent = "";
    searchList.classList.add("hidden");
    return;
  }

  searchList.classList.remove("hidden");

  const conn = await fetch(`/api/v1/beer-styles/${beerStyleName}?offset=0&limit=5`, {
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

async function postBeer(form) {
  const conn = await fetch("/api/v1/beers", {
    method: "POST",
    body: new FormData(form)
  });

  if (!conn.ok) {
    const error = await conn.json();
    console.log(error);
    return;
  }

  const beerId = await conn.json();
  spa(`/beers/${beerId}`);
}

async function updateBeer(form) {
  const beerId = form.beer_id.value;

  const conn = await fetch(`/api/v1/beers/${beerId}`, {
    method: "PUT",
    body: new FormData(form)
  });

  if (!conn.ok) {
    const error = await conn.json();
    console.log(error);
    return;
  }
  // SUCCESS
}

async function deleteBeer(form) {
  const beerId = form.delete_beer_id.value;
  
  const conn = await fetch(`/api/v1/beers/${beerId}`, {
    method: "DELETE",
    body: new FormData(form)
  });

  if (!conn.ok) {
    const error = await conn.json();
    console.log(error);
    return;
  }

  // SUCCESS
  spa(`/beers`);
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
  const elm = event.target.parentElement
  document.querySelector('#beer-name').value = elm.dataset.beer_name
  document.querySelector('#beer-id').value = elm.dataset.beer_id

  const infoHtml = `
  <p class="beer-style">${elm.dataset.beer_style}</p>
  <p class="brewery-name">${elm.dataset.brewery_name}</p>
  <p>
      <span class="alc">ALC.:${elm.dataset.beer_alc}%</span>|
      <span class="ebc">EBC:${elm.dataset.beer_ebc}</span>|
      <span class="ibu">IBU:${elm.dataset.beer_ibu}</span>
  </p>
  `
  document.querySelector(".beer-info").innerHTML = infoHtml

  elm.parentElement.remove()
}

async function postTap(form) {
  const conn = await fetch("/api/v1/taps", {
    method: "POST",
    body: new FormData(form)
  })

  if (!conn.ok) return

  const newTapId = await conn.json()
  spa(`/taps/${newTapId}`)
}

async function updateTap(form) {
  const tapId = form.tap_id.value
  const conn = await fetch(`/api/v1/taps/${tapId}`, {
    method: "PUT",
    body: new FormData(form)
  })

  if (!conn.ok) return

  const res = await conn.json()
  console.log(res)
}

async function deleteTap(form) {
  const tapId = form.tap_id.value
  const conn = await fetch(`/api/v1/taps/${tapId}`, {
    method: "DELETE",
    body: new FormData(form)
  })

  if (!conn.ok) return

  spa("/taps")
}


async function updateBar(form) {
  const barId = form.bar_id.value
  const conn = await fetch(`/api/v1/bars/${barId}`, {
    method: "PUT",
    body: new FormData(form)
  })

  if (!conn.ok) return

  spa(`/bars/${barId}`)
}

async function postBar(form) {
  const conn = await fetch("/api/v1/bars", {
    method: "POST",
    body: new FormData(form)
  })

  if (!conn.ok) return

  const newBarId = await conn.json()
  spa(`/bars/${newBarId}`)
}

async function deleteBar(form) {
  const barId = form.id.value
  const conn = await fetch(`/api/v1/bars/${barId}`, {
    method: "DELETE",
    body: new FormData(form)
  })

  if (!conn.ok) return

  spa("/bars")
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