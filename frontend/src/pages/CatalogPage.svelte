<script>
  import { onMount } from 'svelte';
  import ProductCard from '../components/ProductCard.svelte';
  import ProductDetailModal from '../components/ProductDetailModal.svelte';
  import Link from '../components/Link.svelte';
  import { products } from '../stores/products.js';
  import { cart } from '../stores/cart.js';
  import { isAuthenticated } from '../stores/auth.js';
  import { toasts } from '../lib/toast.js';

  let search = $state('');
  let maxPrice = $state('');
  let statusFilter = $state('all');
  let searching = $state(false);
  let selectedProduct = $state(null);

  const filteredProducts = $derived.by(() => {
    return $products.items.filter(product => {
      const isActive = product.activo ?? true;
      const matchesStatus =
        statusFilter === 'all' ||
        (statusFilter === 'active' && isActive) ||
        (statusFilter === 'inactive' && !isActive);
      const matchesPrice = !maxPrice || product.precio <= Number(maxPrice);
      return matchesStatus && matchesPrice;
    });
  });

  const filteredCount = $derived(filteredProducts.length);

  onMount(async () => {
    if (!$products.items.length) {
      await loadProducts();
    }
  });

  let debounceHandle = null;

  $effect(() => {
    search;
    clearTimeout(debounceHandle);
    debounceHandle = setTimeout(() => {
      loadProducts();
    }, 300);

    return () => clearTimeout(debounceHandle);
  });

  async function loadProducts() {
    try {
      searching = true;
      await products.load(search);
    } catch (error) {
      toasts.push(error.message, 'error');
    } finally {
      searching = false;
    }
  }

  async function add(product) {
    if (!$isAuthenticated) {
      toasts.push('Debes iniciar sesión para usar el carrito.', 'info');
      return;
    }

    try {
      await cart.add(product._id);
      toasts.push(`${product.nombre} añadido al carrito`, 'success');
    } catch (error) {
      toasts.push(error.message, 'error');
    }
  }
</script>

<section class="section-head">
  <div>
    <p class="eyebrow">Catálogo</p>
    <h1>Productos disponibles</h1>
  </div>

  <form class="searchbar" onsubmit={(event) => {
    event.preventDefault();
    loadProducts();
  }}>
    <input type="search" bind:value={search} placeholder="Buscar por nombre..." aria-label="Buscar productos" />
    <button class="primary" type="submit" disabled={searching}>Buscar</button>
  </form>
</section>

<section class="grid two">
  <div class="panel compact">
    <label for="statusFilter">Estado</label>
    <select id="statusFilter" bind:value={statusFilter}>
      <option value="all">Todos</option>
      <option value="active">Activos</option>
      <option value="inactive">No activos</option>
    </select>
  </div>

  <div class="panel compact">
    <label for="maxPrice">Precio máximo</label>
    <input id="maxPrice" type="number" min="0" step="0.01" bind:value={maxPrice} placeholder="Sin límite" />
  </div>
</section>

<div class="panel compact">
  <strong>{filteredCount}</strong> productos visibles tras aplicar filtros.
</div>

{#if $products.loading}
  <div class="panel">Cargando productos...</div>
{:else if !$products.items.length}
  <div class="panel empty-state">
    <h2>No hay productos</h2>
    <p>Si eres administrador podrás crear el primero desde el panel de administración.</p>
    <Link href="/admin" className="text-link">Ir a administración</Link>
  </div>
{:else if !filteredProducts.length}
  <div class="panel empty-state">
    <h2>No hay resultados con esos filtros</h2>
    <p>Prueba a limpiar la búsqueda o ampliar el precio máximo.</p>
  </div>
{:else}
  <section class="product-grid">
    {#each filteredProducts as product (product._id)}
      <ProductCard {product} onAdd={add} onView={(value) => (selectedProduct = value)} />
    {/each}
  </section>
{/if}

<ProductDetailModal
  product={selectedProduct}
  canAdd={$isAuthenticated}
  onAdd={add}
  onClose={() => (selectedProduct = null)}
/>
