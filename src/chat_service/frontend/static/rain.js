// Export constants that you want to share
export const IMAGE_URL = 'https://content.mycutegraphics.com/graphics/food/pepperoni-pizza-slice.png';
export const MAX_DROPS = 100; // Max number of images on screen at once
export const DROP_INTERVAL = 200; // Milliseconds between new drops

export const rainContainer = document.getElementById('rainContainer');
let rainIntervalId = null;

// Function to create a single raindrop image element
function createRaindrop() {
    const raindrop = document.createElement('img');
    raindrop.src = IMAGE_URL;
    raindrop.classList.add('raindrop-image');
    raindrop.alt = 'Raindrop'; 

    // Randomize starting X position
    const startX = Math.random() * window.innerWidth;
    raindrop.style.left = `${startX}px`;

    // Randomize animation duration for varying speeds
    const duration = Math.random() * (10 - 5) + 5; // Between 5 and 10 seconds
    raindrop.style.animationDuration = `${duration}s`;

    // Randomize animation delay to stagger drops
    const delay = Math.random() * 5;
    raindrop.style.animationDelay = `${delay}s`;

    raindrop.style.animationName = 'fall';
    rainContainer.appendChild(raindrop);

    // Remove the raindrop after its animation finishes to prevent memory leaks
    raindrop.addEventListener('animationend', () => {
        raindrop.remove();
    });
}

// start the rain effect
export function startRain() {
    if (rainIntervalId === null) {
        rainIntervalId = setInterval(() => {
            if (rainContainer.children.length < MAX_DROPS) {
                createRaindrop();
            }
        }, DROP_INTERVAL);
    }
}

// stop the rain if needed
export function stopRain() {
    if (rainIntervalId !== null) {
        clearInterval(rainIntervalId);
        rainIntervalId = null;
    }
}
