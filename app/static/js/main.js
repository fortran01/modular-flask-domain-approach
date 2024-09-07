document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");
  const logoutBtn = document.getElementById("logoutBtn");
  const checkPointsBtn = document.getElementById("checkPointsBtn");
  const pointsDisplay = document.getElementById("pointsDisplay");
  const checkoutBtn = document.getElementById("checkoutBtn");
  const checkoutResult = document.getElementById("checkoutResult");
  const shoppingCart = document.getElementById("shoppingCart");

  if (loginForm) {
    loginForm.addEventListener("submit", handleLogin);
  }

  if (logoutBtn) {
    logoutBtn.addEventListener("click", handleLogout);
  }

  if (checkPointsBtn) {
    checkPointsBtn.addEventListener("click", handleCheckPoints);
  }

  if (checkoutBtn) {
    checkoutBtn.addEventListener("click", handleCheckout);
  }

  // Add event listeners for "Add to Cart" buttons
  const addToCartButtons = document.querySelectorAll(".addToCartBtn");
  addToCartButtons.forEach((button) => {
    button.addEventListener("click", handleAddToCart);
  });

  // Load the shopping cart on page load
  if (shoppingCart) {
    loadShoppingCart();
  }

  async function handleLogin(event) {
    event.preventDefault();
    const customerId = document.getElementById("customerIdInput").value;
    try {
      const response = await fetch("/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ customer_id: customerId }),
      });
      const data = await response.json();
      if (data.success) {
        window.location.reload();
      } else {
        alert("Login failed. Please try again.");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }

  async function handleLogout() {
    try {
      await fetch("/logout");
      window.location.reload();
    } catch (error) {
      console.error("Error:", error);
    }
  }

  async function handleCheckPoints() {
    try {
      const response = await fetch("/points");
      const data = await response.json();
      pointsDisplay.textContent = `Your current points: ${data.points}`;
    } catch (error) {
      console.error("Error:", error);
    }
  }

  async function handleAddToCart(event) {
    const productId = event.target.getAttribute("data-product-id");
    try {
      const response = await fetch("/cart", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ productId: parseInt(productId), quantity: 1 }),
      });
      if (response.ok) {
        loadShoppingCart();
      } else {
        alert("Failed to add item to cart. Please try again.");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }

  async function loadShoppingCart() {
    try {
      const response = await fetch("/cart");
      const cart = await response.json();
      updateShoppingCartDisplay(cart);
    } catch (error) {
      console.error("Error:", error);
    }
  }

  function updateShoppingCartDisplay(cart) {
    shoppingCart.innerHTML = "";
    if (cart.items && cart.items.length > 0) {
      const cartList = document.createElement("ul");
      cart.items.forEach((item) => {
        const listItem = document.createElement("li");
        listItem.className = "flex justify-between items-center mb-2";
        listItem.innerHTML = `
                  <span>${item.product.name} - Quantity: ${item.quantity}</span>
                  <div>
                      <button class="updateQuantityBtn bg-blue-500 text-white px-2 py-1 rounded" data-product-id="${item.product.id}" data-action="increase">+</button>
                      <button class="updateQuantityBtn bg-blue-500 text-white px-2 py-1 rounded" data-product-id="${item.product.id}" data-action="decrease">-</button>
                      <button class="removeFromCartBtn bg-red-500 text-white px-2 py-1 rounded" data-product-id="${item.product.id}">Remove</button>
                  </div>
              `;
        cartList.appendChild(listItem);
      });
      shoppingCart.appendChild(cartList);

      // Add event listeners for update quantity and remove buttons
      const updateQuantityButtons =
        document.querySelectorAll(".updateQuantityBtn");
      updateQuantityButtons.forEach((button) => {
        button.addEventListener("click", handleUpdateQuantity);
      });

      const removeFromCartButtons =
        document.querySelectorAll(".removeFromCartBtn");
      removeFromCartButtons.forEach((button) => {
        button.addEventListener("click", handleRemoveFromCart);
      });
    } else {
      shoppingCart.textContent = "Your cart is empty.";
    }
  }

  async function handleUpdateQuantity(event) {
    const productId = event.target.getAttribute("data-product-id");
    const action = event.target.getAttribute("data-action");
    const productItem = event.target.closest("li");
    const quantityDisplay = productItem.querySelector("span");
    let currentQuantity = parseInt(
      quantityDisplay.textContent.match(/Quantity: (\d+)/)[1]
    );

    const newQuantity =
      action === "increase"
        ? currentQuantity + 1
        : Math.max(0, currentQuantity - 1);

    try {
      const response = await fetch(`/cart/${productId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ quantity: newQuantity }),
      });

      if (response.ok) {
        quantityDisplay.textContent = `Quantity: ${newQuantity}`;
        loadShoppingCart();
      } else {
        alert("Failed to update quantity. Please try again.");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }

  async function handleRemoveFromCart(event) {
    const productId = event.target.getAttribute("data-product-id");
    try {
      const response = await fetch(`/cart/${productId}`, {
        method: "DELETE",
      });
      if (response.ok) {
        loadShoppingCart();
      } else {
        alert("Failed to remove item from cart. Please try again.");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }

  async function handleCheckout() {
    try {
      const response = await fetch("/checkout", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await response.json();
      checkoutResult.textContent = `Checkout complete. Total points earned: ${data.total_points_earned}`;
      loadShoppingCart(); // Refresh the cart after checkout
    } catch (error) {
      console.error("Error:", error);
      checkoutResult.textContent = "Checkout failed. Please try again.";
    }
  }
});
