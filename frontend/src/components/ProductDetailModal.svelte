<script>
  import { UPLOADS_URL } from '../config.js';

  let { product = null, onClose = null, onAdd = null, canAdd = false } = $props();

  const imageUrl = $derived(product?.imagen ? `${UPLOADS_URL}/${product.imagen}` : null);
  const statusLabel = $derived((product?.activo ?? true) ? 'Activo' : 'No activo');
</script>

{#if product}
  <div
    class="modal-backdrop"
    role="button"
    aria-label="Cerrar detalle de producto"
    tabindex="0"
    onclick={onClose}
    onkeydown={(event) => {
      if (event.key === 'Escape' || event.key === 'Enter' || event.key === ' ') {
        onClose?.();
      }
    }}
  >
    <div
      class="modal-card"
      role="dialog"
      aria-modal="true"
      aria-label={`Detalle de ${product.nombre}`}
      tabindex="-1"
      onclick={(event) => event.stopPropagation()}
      onkeydown={(event) => event.stopPropagation()}
    >
      <div class="modal-media">
        {#if imageUrl}
          <img src={imageUrl} alt={product.nombre} />
        {:else}
          <div class="product-placeholder">Sin imagen</div>
        {/if}
      </div>

      <div class="stack">
        <div>
          <p class="eyebrow">Detalle</p>
          <h2>{product.nombre}</h2>
        </div>

        <div class="detail-grid">
          <div class="panel compact">
            <span class="muted">Precio</span>
            <strong>{product.precio.toFixed(2)} €</strong>
          </div>
          <div class="panel compact">
            <span class="muted">Estado</span>
            <strong>{statusLabel}</strong>
          </div>
        </div>

        <p class="muted">
          El backend actual no expone más campos de detalle, así que esta vista muestra la información real disponible en la API.
        </p>

        <div class="card-actions">
          {#if canAdd}
            <button class="primary" type="button" onclick={() => onAdd?.(product)}>Añadir al carrito</button>
          {/if}
          <button class="secondary" type="button" onclick={onClose}>Cerrar</button>
        </div>
      </div>
    </div>
  </div>
{/if}
