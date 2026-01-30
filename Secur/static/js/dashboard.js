const sidebar = document.querySelector(".SIDEBAR")
const dashToggle = document.querySelector(".Toggle")

// Toggle sidebar when button is clicked
dashToggle.addEventListener('click', function(event){
  sidebar.classList.toggle("hide")
})

// Close sidebar when clicking outside
document.addEventListener('click', function(event){
  const clickedToggle = dashToggle.contains(event.target)
  const clickedSidebar = sidebar.contains(event.target)
  
  // If click was outside both sidebar AND toggle button
  if (!clickedSidebar && !clickedToggle && !sidebar.classList.contains('hide')) {
    sidebar.classList.add('hide')
  }
})

