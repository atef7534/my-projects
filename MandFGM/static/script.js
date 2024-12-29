function addMWord(myclass) {
  let content = document.querySelector(`.${myclass === 0 ? "m" : "f"}-words .content`);
  let child = document.createElement('p');

  child.classList.add(myclass === 0 ? "m" : "f");
  child.setAttribute('contenteditable', 'true');
  
  // Generate a unique ID for the new element
  let newId = Date.now();  
  child.setAttribute('data-id', newId);
  content.appendChild(child);

  let timeout = null;

  child.addEventListener("input", function() {
      clearTimeout(timeout);

      timeout = setTimeout(() => {
          let id = child.getAttribute("data-id");
          let data = child.textContent.trim();

          if (data) {
              fetch("/add", {
                  method: "POST",
                  headers: {
                      'Content-Type': 'application/json'
                  },
                  body: JSON.stringify({
                      id: id,
                      data: data,
                      type: myclass
                  })
              })
              .then(response => response.json())
              .then(data => {
                  if (data.success) {
                      console.log("Data updated successfully!");
                  } else {
                      console.error("Error updating data:", data.error);
                  }
              })
              .catch(error => console.error('Fetch error:', error));
          }
      }, 500);  // Debounce to limit the frequency of requests
  });
}

function handleRemove(position) {
  fetch("/remove", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      id: position.getAttribute("data-id")
    })
  })
  .then(response => response.json())
  .then(response => {
    if (response.success) {
      console.log("Removed, successfully!");
    } else {
      console.log("Error removing data: ", response.error);
    }
  })
  .catch(error => console.error("Fetch Error: ", error));
  position.remove();
}

function handleLnk() {
  let links = document.querySelectorAll(".lnk");
  links.forEach(lnk => {
    lnk.addEventListener("click", function() {
      clearActive(links);
      lnk.classList.add("active");
      // TODO: ...
    });
  });
}

function clearActive(lnks) {
  lnks.forEach(lnk => {
    lnk.classList.remove("active");
  });
}

function handleVerb(target) {
  let inps = target.querySelectorAll("input.inp");
  let verbGM = inps[0].value;
  let verbAR = inps[1].value;
  
  fetch("/addverb", {
    method: "POST", 
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      id: Date.now(),
      verbGM: verbGM,
      verbAR: verbAR
    })
  })
  .then(response => response.json())
  .then(response => {
    if (response.success) {
      console.log("Successfully added!");
      inps[0].value = '';
      inps[1].value = '';
    } else {
      console.log(`Error adding your verb, ${response.error}`);
    }
  })
  .catch(response => console.log("Fetch Error: ", response));
}

function handleSen(target) {
  const childs = target.children;
  let inpGM = childs[0];
  let inpAR = childs[1];

  fetch("/addsentence", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      id: Date.now(),
      senGM: inpGM.value.toLowerCase(),
      senAR: inpAR.value
    })
  })
  .then(res => res.json())
  .then(res => {
    if (res.success) {
      console.log("Successfully added new sentence!");
      inpGM.value = "";
      inpAR.value = "";
      inpGM.focus();
    } else {
      console.log(`Failed to add your sentence and the error is ${res.error}`)
    }
  })
  .catch(res => console.log(`Fetch Error ${res}`));
}

// Calling our functions
handleLnk();

let timer = null;
function editSentence(id, content, type) {
  clearTimeout(timer);
  timer = setTimeout(function () {
    fetch("/editsentence", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        id: id,
        content: content,
        type: type
      })
    })
    .then(res => res.json())
    .then(res => {
      if (res.success) {
        console.log("edited!");
      } else {
        console.log(res.error);
      }
    })
    .catch(res => console.log(res));
  }, 400);
}