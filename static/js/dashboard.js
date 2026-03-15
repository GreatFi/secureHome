const sidebar = document.querySelector(".luxury-sidebar");
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
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${protocol}//${window.location.host}/ws/notifications/`);
    
    ws.onopen = () => {};
    
    ws.onmessage = (e) => {
        const data = JSON.parse(e.data);
        
        // Update bell badge
        const badge = document.querySelector('.notification-badge');
        if (badge) {
            const currentCount = parseInt(badge.textContent) || 0;
            badge.textContent = currentCount + 1;
            badge.classList.remove('hidden');
        }
        
        // Optional: Show toast notification
        alert(`New notification: ${data.message}`);
    };
    
    ws.onerror = (e) => {};
    ws.onclose = () => {};
