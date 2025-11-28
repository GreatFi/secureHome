// const links = document.querySelector(".nav-links")
// const btn = document.querySelector(".BARS")
// const cancel = document.querySelector(".cancel")

// btn.addEventListener("click", (event) => {
//     links.classList.toggle("hide") 
// })


document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll(".sidebarlink");
  const content = document.querySelector(".content");

  // Function to load content dynamically
  function loadPage(url, addToHistory = true) {
    // Add ?partial=1 so Django knows to send only partial content
    const fetchUrl = url.includes("?") ? `${url}&partial=1` : `${url}?partial=1`;

    fetch(fetchUrl, {
      headers: { "X-Requested-With": "XMLHttpRequest" },
      credentials: "same-origin",
    })
      .then(response => {
        if (!response.ok) throw new Error("Network error");
        return response.text();
      })
      .then(html => {
        // Replace dashboard content
        content.innerHTML = html;
        document.querySelector(".content").innerHTML = html;
        console.log("Updated dashboard", html);
        
        // Update browser URL without reloading
        if (addToHistory) history.pushState(null, "", url);
      })
      .catch(error => {
        console.error("Error loading section:", error);
        content.innerHTML = "<p>Failed to load section.</p>";
      });
  }

  // Sidebar link click events
  links.forEach(link => {
    link.addEventListener("click", event => {
      event.preventDefault();
      const url = link.getAttribute("href");
      loadPage(url); // load section dynamically

      // Highlight the active link
      links.forEach(l => l.classList.remove("active"));
      link.classList.add("active");
    });
  });

  // Handle browser back/forward navigation
  window.addEventListener("popstate", () => {
    loadPage(location.pathname, false);
  });
});


// Add event listener to a parent container
document.addEventListener("submit", async (event) => {
  if (event.target.classList.contains("likeform")) {
    event.preventDefault();
    
    const likeform = event.target;
    const likebtn = likeform.querySelector(".like");
    const FormLike = new FormData(likeform);

    try {
      const response = await fetch(likeform.action, {
        method: "POST",
        body: FormLike,
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": likeform.querySelector("[name=csrfmiddlewaretoken]").value,
        },
      });

      const data = await response.json();

      if (data.success && data.is_saved) {
        likebtn.innerHTML = "❤️ Saved";
        // location.reload()
      } else {
        likebtn.innerHTML = "Save";
        location.reload()
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }
});



// const tl = gsap.timeline({

//     defaults : {
//         opacity : 0,
//         ease : "linear",
//         duration : 1
//     }
// })

// tl.fromTo(".hero-text", {y : 100}, {
//     opacity : 1,
//     y : 0
// })
// tl.fromTo(".subtext", {y : 100}, {
//     opacity : 1,
//     y : 0
// })
// tl.fromTo(".hero-btn", {y : 100}, {
//     opacity : 1,
//     y : 0
// })
// tl.fromTo(".hero-cards", {y : 100}, {
//     opacity : 1,
//     y : 0
// })


// const login = gsap.timeline({
//     defaults : {
//         opacity : 0,
//         ease : "linear",
//         duration : 2
//     }
// })

// login.fromTo(".login-logo", {x:100}, {
//     opacity : 1,
//     x : 0
// })

// login.fromTo(".login-cont", {x:100}, {
//     opacity : 1,
//     x : 0
// })


