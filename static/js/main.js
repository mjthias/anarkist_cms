
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

  if (!conn.status == 200) {
    console.log("Can't connect to endpoint");
    return;
  }
  const html = await conn.text();

  // Remove old data
  document.querySelector(`[data-page_url="${memoUrl}"]`).remove();
  // Append the new data and set dataset-spa_url
  document.querySelector("main").insertAdjacentHTML("afterbegin", html);

  // Get and set title
  const title = document.querySelector(`[data-page_url="${spaUrl}"]`).dataset.page_title;
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