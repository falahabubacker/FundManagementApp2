document.addEventListener('DOMContentLoaded', function () {
    const increaseFontButton = document.getElementById('increase-font');
    const decreaseFontButton = document.getElementById('decrease-font');
    const minFontSize = 0.8; // Prevents text from becoming too small
    const maxFontSize = 2.5; // Prevents text from becoming too large
    let currentFontSize = parseFloat(localStorage.getItem('font-size')) || 1.1;

    function updateFontSize() {
        document.body.style.fontSize = currentFontSize + 'em';
        localStorage.setItem('font-size', currentFontSize);
    }

    if (increaseFontButton && decreaseFontButton) {
        increaseFontButton.addEventListener('click', function () {
            if (currentFontSize < maxFontSize) {
                currentFontSize = parseFloat((currentFontSize + 0.1).toFixed(1));
                updateFontSize();
            }
        });

        decreaseFontButton.addEventListener('click', function () {
            if (currentFontSize > minFontSize) {
                currentFontSize = parseFloat((currentFontSize - 0.1).toFixed(1));
                updateFontSize();
            }
        });
    }

    updateFontSize(); // Apply saved font size on page load
});
