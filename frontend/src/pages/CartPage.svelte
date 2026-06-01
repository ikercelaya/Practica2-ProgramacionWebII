<script>
  import { onMount } from 'svelte';
  import { cart, cartTotal } from '../stores/cart.js';
  import { currentUser } from '../stores/auth.js';
  import { orders } from '../stores/orders.js';
  import { router } from '../lib/router.js';
  import { toasts } from '../lib/toast.js';

  let checkoutLoading = $state(false);

  onMount(async () => {
    try {
      await cart.load();
    } catch (error) {
      toasts.push(error.message, 'error');
    }
  });

  async function remove(item) {
    try {
      await cart.remove(item.productId._id);
      toasts.push(`${item.productId.nombre} eliminado del carrito`, 'success');
    } catch (error) {
      toasts.push(error.message, 'error');
    }
  }

  async function checkout() {
    if (!$cart.items.length) return;

    if (!window.confirm('¿Confirmas que quieres finalizar la compra?')) {
      return;
    }

    checkoutLoading = true;

    try {
      const order = orders.createOrder({
        user: $currentUser,
        items: $cart.items,
        total: $cartTotal
      });
      await cart.checkout();
      toasts.push(`Pedido ${order.id} realizado correctamente`, 'success');
      router.go('/pedidos');
    } catch (error) {
      toasts.push(error.message, 'error');
    } finally {
      checkoutLoading = false;
    }
  }
</script>

<section class="section-head">
  <div>
    <p class="eyebrow">Carrito</p>
    <h1>Tus productos seleccionados</h1>
  </div>
  <div class="panel compact total-box">
    <span>Total</span>
    <strong>{$cartTotal.toFixed(2)} EUR</strong>
  </div>
</section>

{#if $cart.loading}
  <div class="panel">Cargando carrito...</div>
{:else if !$cart.items.length}
  <div class="panel empty-state">
    <h2>El carrito esta vacio</h2>
    <p>Vuelve al catalogo y añade algun producto para probar la API.</p>
  </div>
{:else}
  <section class="stack">
    {#each $cart.items as item (item.productId._id)}
      <article class="panel cart-row">
        <div>
          <p class="eyebrow">Cantidad {item.quantity}</p>
          <h3>{item.productId.nombre}</h3>
        </div>
        <strong>{(item.productId.precio * item.quantity).toFixed(2)} EUR</strong>
        <button class="danger" type="button" onclick={() => remove(item)}>Quitar</button>
      </article>
    {/each}
  </section>

  <section class="checkout-bar">
    <div class="panel compact total-box">
      <span>Total pedido</span>
      <strong>{$cartTotal.toFixed(2)} EUR</strong>
    </div>
    <button class="primary checkout-button" type="button" onclick={checkout} disabled={checkoutLoading || $cart.loading}>
      {checkoutLoading ? 'Procesando compra...' : 'Finalizar compra'}
    </button>
  </section>
{/if}
