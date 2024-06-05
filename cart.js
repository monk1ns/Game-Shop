let cart = [];
function addToCart(product) {
    cart.push(product);
    updateCartDisplay(); // Вызываем функцию для обновления отображения корзины
}
function updateCartDisplay() {
    const cartItemsSection = document.querySelector('.cart-items');
    cartItemsSection.innerHTML = ''; // Очищаем старые элементы

    cart.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.classList.add('cart-item');

        const img = document.createElement('img');
        img.src = item.imageSrc;
        img.alt = item.title;

        const infoDiv = document.createElement('div');
        infoDiv.innerHTML = `
            <h3>${item.title}</h3>
            <p>Platform: ${item.platform}</p>
            <p>Genre: ${item.genre}</p>
        `;

        const actionsDiv = document.createElement('div');
        actionsDiv.innerHTML = `
            <span class="item-price">€${item.price.toFixed(2)}</span>
            <button class="remove-btn">Remove</button>
        `;

        itemElement.appendChild(img);
        itemElement.appendChild(infoDiv);
        itemElement.appendChild(actionsDiv);

        cartItemsSection.appendChild(itemElement);
    });

    // Обновляем общую стоимость и количество товаров в корзине
    const totalPriceSpan = document.querySelector('.total-price');
    const itemCountSpan = document.querySelector('[data-item-count]');
    totalPriceSpan.textContent = `Total: €${cart.reduce((acc, curr) => acc + curr.price, 0).toFixed(2)}`;
    itemCountSpan.textContent = `Your Cart (${cart.length} items)`;
}
function checkAuthStatus() {
    const authLink = document.getElementById('auth-link');
    const token = getCookie('token');

    if (token) {
        authLink.textContent = 'LOGOUT';
        authLink.onclick = logout; // Установите обработчик события logout
    } else {
        authLink.textContent = 'LOGIN';
        authLink.onclick = login; // Установите обработчик события login
    }
}

// Функция для получения значения cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Предположим, что функции login и logout уже определены где-то в вашем коде
function login() {
    // Логика входа в систему
}

function logout() {
    // Логика выхода из системы
}

// Вызовите функцию checkAuthStatus при загрузке страницы
window.onload = checkAuthStatus;