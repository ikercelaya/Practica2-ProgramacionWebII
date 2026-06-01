<script>
  import { UPLOADS_URL } from '../config.js';

  let { product = null, mode = 'create', busy = false, onSubmit } = $props();

  let selectedFile = null;

  const currentImageUrl = $derived(product?.imagen ? `${UPLOADS_URL}/${product.imagen}` : null);

  function submit(event) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    if (!selectedFile) {
      formData.delete('imagen');
    }

    onSubmit?.({
      formData,
      values: {
        nombre: String(formData.get('nombre') || ''),
        precio: Number(formData.get('precio') || 0)
      }
    });
  }
</script>

<form class="panel form-grid" onsubmit={submit}>
  <div>
    <label for="nombre">Nombre</label>
    <input id="nombre" name="nombre" type="text" required value={product?.nombre || ''} />
  </div>

  <div>
    <label for="precio">Precio</label>
    <input id="precio" name="precio" type="number" step="0.01" min="0" required value={product?.precio || ''} />
  </div>

  <div class="full">
    <label for="imagen">
      Imagen{mode === 'edit' ? ' (opcional: elige una nueva para reemplazar la actual)' : ''}
    </label>

    {#if mode === 'edit'}
      {#if currentImageUrl}
        <img class="form-image-preview" src={currentImageUrl} alt={product?.nombre} />
      {:else}
        <p class="muted">Este producto no tiene imagen todavía.</p>
      {/if}
    {/if}

    <input
      id="imagen"
      name="imagen"
      type="file"
      accept="image/*"
      onchange={(event) => {
        selectedFile = event.currentTarget.files?.[0] || null;
      }}
    />
  </div>

  <div class="full">
    <button class="primary" type="submit" disabled={busy}>
      {busy ? 'Guardando...' : mode === 'create' ? 'Crear producto' : 'Actualizar producto'}
    </button>
  </div>
</form>

<style>
  .form-image-preview {
    max-width: 140px;
    max-height: 140px;
    object-fit: cover;
    border-radius: 12px;
    display: block;
    margin-bottom: 0.5rem;
  }
</style>
