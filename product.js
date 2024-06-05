document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', () => {
        const productInfo = {
            id: Math.random(), // Генерируем уникальный ID для каждого товара
            title: button.parentElement.nextElementSibling.querySelector('h2').textContent,
            imageSrc: button.parentElement.nextElementSibling.previousElementSibling.src,
            genre: button.parentElement.nextElementSibling.querySelector('p').textContent.split(':')[1].trim(),
            price: parseFloat(button.parentElement.nextElementSibling.querySelector('p').textContent.replace('€', '').replace(',', '.'))
        };
        addToCart(productInfo);
    });
});
// Структура корзины
let cart = [];

// Функция для добавления товара в корзину
function addToCart(product) {
    // Проверяем, есть ли уже этот товар в корзине
    let existingProduct = cart.find(item => item.id === product.id);
    if (existingProduct) {
        // Увеличиваем количество существующего товара
        existingProduct.quantity++;
    } else {
        // Добавляем новый товар в корзину
        cart.push({...product, quantity: 1});
    }

    // Обновляем интерфейс корзины
    updateCart();
}

// Функция для обновления интерфейса корзины
function updateCart() {
    const cartItemsElement = document.getElementById('cart-items');
    cartItemsElement.innerHTML = ''; // Очищаем список товаров в корзине

    cart.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.title} - ${item.quantity}`;
        cartItemsElement.appendChild(li);
    });

    // Добавляем кнопку очистки корзины, если она еще не добавлена
    if (!document.getElementById('clear-cart')) {
        const clearCartButton = document.createElement('button');
        clearCartButton.textContent = 'Clear Cart';
        clearCartButton.addEventListener('click', clearCart);
        document.getElementById('cart-container').appendChild(clearCartButton);
    }
}

// Функция для очистки корзины
function clearCart() {
    cart = [];
    updateCart(); // Обновляем интерфейс корзины
}

// Чтение данных из products.json и заполнение корзины тестовыми данными
async function initializeCart() {
    const response = await fetch('products.json');
    const products = await response.json();
    products.forEach(product => {
        addToCart(product); // Добавляем каждый продукт в корзину
    });
}

initializeCart();
