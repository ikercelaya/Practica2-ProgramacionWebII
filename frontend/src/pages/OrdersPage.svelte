<script>
  import { orders } from '../stores/orders.js';

  function formatDate(value) {
    return new Date(value).toLocaleString('es-ES');
  }
</script>

<section class="section-head">
  <div>
    <p class="eyebrow">Pedidos</p>
    <h1>Historial de compras</h1>
  </div>
</section>

{#if !$orders.items.length}
  <div class="panel empty-state">
    <h2>Todavía no has realizado ningún pedido</h2>
    <p>Cuando finalices una compra desde el carrito, aparecerá aquí guardada como simulación de pedido.</p>
  </div>
{:else}
  <section class="stack">
    {#each $orders.items as order (order.id)}
      <article class="panel stack">
        <div class="order-head">
          <div>
            <p class="eyebrow">{order.id}</p>
            <h2>Pedido realizado el {formatDate(order.createdAt)}</h2>
          </div>
          <strong>{order.total.toFixed(2)} €</strong>
        </div>

        <div class="stack">
          {#each order.items as item}
            <div class="order-row">
              <div>
                <strong>{item.nombre}</strong>
                <p class="muted">Cantidad: {item.quantity}</p>
              </div>
              <span>{(item.precio * item.quantity).toFixed(2)} €</span>
            </div>
          {/each}
        </div>
      </article>
    {/each}
  </section>
{/if}
