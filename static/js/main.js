
//SPA
// Init state - the first loaded page
history.replaceState({ spaUrl: location.pathname }, "", location.pathname);
let memoUrl = location.pathname;

async function spa(spaUrl, doPushState = true) {
  // if new and current url are same - end
  // if (spaUrl == memoUrl) return;
  // Fetch spaUrl if not in DOMM
  const conn = await fetch(spaUrl, {
    method: "GET",
    headers: { spa: true },
  });

  if (!conn.ok) {
    const url = errorUrl(spaUrl, conn.status);
    spa(url);
    return;
  } 
  const html = await conn.text();

  // Remove old data
  document.querySelector(`[data-page_url="${cleanUrl(memoUrl)}"]`).remove();
  // Append the new data and set dataset-spa_url
  document.querySelector("main").insertAdjacentHTML("afterbegin", html);

  // Get and set title
  const title = document.querySelector(`[data-page_url="${cleanUrl(spaUrl)}"]`).dataset.page_title;
  document.querySelector("title").textContent = title;

  // Memo the appended url
  memoUrl = spaUrl;

  // Push state
  if (doPushState) {
    history.pushState({ spaUrl: spaUrl }, "", spaUrl);
  }
}

// History back/forth
window.addEventListener("popstate", (e) => {
  spa(e.state.spaUrl, false);
});

function errorUrl(spaUrl, status) {
    url = spaUrl.replace("/", "");
    return `/${status}?url=${url}`;
}

function cleanUrl(url) {
  if (url.includes("?")) {
    url = url.substring(0, url.indexOf("?"))
  } 
  return url;
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
  searchTerm = event.target.value;
  console.log(searchTerm);
  if (searchTerm.length < 2) {
    return;
  }

  const conn = await fetch(`/api/v1/breweries/${searchTerm}?offset=0&limit=5`, {
    method: "GET"
  });
  const resp = await conn.json();
  if (!conn.ok) {
    // TODO: Handle error
    console.log(resp);
    return;
  }

  // TODO: Handle multiple results, and display to the user
  
  if (resp.length === 1) {
    document.querySelector("#brewery_id").value = resp[0].brewery_id;
  }
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
  searchTerm = event.target.value;
  console.log(searchTerm);
  if (searchTerm.length < 2) {
    return;
  }

  const conn = await fetch(`/api/v1/beer-styles/${searchTerm}?offset=0&limit=5`, {
    method: "GET"
  });
  const resp = await conn.json();
  if (!conn.ok) {
    // TODO: Handle error
    console.log(resp);
    return;
  }

  // TODO: Handle multiple results, and display to the user

  if (resp.length === 1) {
    document.querySelector("#beer_style_id").value = resp[0].beer_style_id;
  }
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
  searchList.textContent = ""

  if (beerName.length < 2) {
    return
  }

  const conn = await fetch(`/api/v1/beers?name=${beerName}`, {
    headers: {as_html : true}
  })

  if (!conn.ok) return

  const html = await conn.text()
  searchList.insertAdjacentHTML("afterbegin", html)
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