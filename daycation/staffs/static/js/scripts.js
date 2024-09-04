function showModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.style.display = "block";
}

function hideModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.style.display = "none";
}

// Close the modals when clicking outside of them
window.onclick = function(event) {
    var modals = document.getElementsByClassName('modal');
    for (var i = 0; i < modals.length; i++) {
        if (event.target == modals[i]) {
            modals[i].style.display = "none";
        }
    }
}
