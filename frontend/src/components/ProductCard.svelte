<script>
  import { UPLOADS_URL } from '../config.js';

  let { product, isAdminView = false, onAdd = null, onEdit = null, onDelete = null, onView = null } = $props();

  const imageUrl = $derived(product.imagen ? `${UPLOADS_URL}/${product.imagen}` : null);
  const statusLabel = $derived((product.activo ?? true) ? 'Activo' : 'No activo');
</script>

<article class="card product-card">
  <div class="product-image">
    {#if imageUrl}
      <img src={imageUrl} alt={product.nombre} />
    {:else}
      <div class="product-placeholder">Sin imagen</div>
    {/if}
  </div>

  <div class="product-info">
    <div>
      <p class="eyebrow">Producto</p>
      <h3>{product.nombre}</h3>
      <p class="muted">{statusLabel}</p>
    </div>
    <strong class="price">{product.precio.toFixed(2)} €</strong>
  </div>

  <div class="card-actions">
    <button type="button" class="secondary" onclick={() => onView?.(product)}>Ver detalle</button>
    {#if isAdminView}
      <button type="button" class="secondary" onclick={() => onEdit?.(product)}>Editar</button>
      <button type="button" class="danger" onclick={() => onDelete?.(product)}>Eliminar</button>
    {:else}
      <button type="button" class="primary" onclick={() => onAdd?.(product)}>Añadir al carrito</button>
    {/if}
  </div>
</article>
