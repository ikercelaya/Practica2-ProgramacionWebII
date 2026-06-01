<script>
  import { onMount } from 'svelte';
  import ProductCard from '../components/ProductCard.svelte';
  import ProductDetailModal from '../components/ProductDetailModal.svelte';
  import ProductForm from '../components/ProductForm.svelte';
  import UserForm from '../components/UserForm.svelte';
  import { api } from '../lib/api.js';
  import { products } from '../stores/products.js';
  import { users } from '../stores/users.js';
  import { toasts } from '../lib/toast.js';

  let productBusy = $state(false);
  let userBusy = $state(false);
  let selectedProduct = $state(null);
  let selectedUser = $state(null);
  let viewedProduct = $state(null);

  onMount(async () => {
    await Promise.all([reloadProducts(), reloadUsers()]);
  });

  async function reloadProducts() {
    try {
      await products.load();
    } catch (error) {
      toasts.push(error.message, 'error');
    }
  }

  async function reloadUsers() {
    try {
      await users.load();
    } catch (error) {
      toasts.push(error.message, 'error');
    }
  }

  async function handleCreateProduct(payload) {
    productBusy = true;
    try {
      await api.createProduct(payload.formData);
      toasts.push('Producto creado correctamente', 'success');
      await reloadProducts();
    } catch (error) {
      toasts.push(error.message, 'error');
    } finally {
      productBusy = false;
    }
  }

  async function handleUpdateProduct(payload) {
    productBusy = true;
    try {
      await api.updateProduct(selectedProduct._id, payload.values);
      toasts.push('Producto actualizado correctamente', 'success');
      selectedProduct = null;
      await reloadProducts();
    } catch (error) {
      toasts.push(error.message, 'error');
    } finally {
      productBusy = false;
    }
  }

  async function deleteProduct(product) {
    if (!window.confirm(`¿Eliminar "${product.nombre}"?`)) return;

    try {
      await api.deleteProduct(product._id);
      toasts.push('Producto eliminado', 'success');
      await reloadProducts();
    } catch (error) {
      toasts.push(error.message, 'error');
    }
  }

  async function handleCreateUser(payload) {
    userBusy = true;
    try {
      await api.createUser(payload);
      toasts.push('Usuario creado correctamente', 'success');
      await reloadUsers();
    } catch (error) {
      toasts.push(error.message, 'error');
    } finally {
      userBusy = false;
    }
  }

  async function handleUpdateUser(payload) {
    userBusy = true;
    try {
      const request = { ...payload };
      if (!request.password) delete request.password;
      await api.updateUser(selectedUser._id, request);
      toasts.push('Usuario actualizado correctamente', 'success');
      selectedUser = null;
      await reloadUsers();
    } catch (error) {
      toasts.push(error.message, 'error');
    } finally {
      userBusy = false;
    }
  }

  async function deleteUser(user) {
    if (!window.confirm(`¿Eliminar al usuario "${user.username}"?`)) return;

    try {
      await api.deleteUser(user._id);
      toasts.push('Usuario eliminado', 'success');
      await reloadUsers();
    } catch (error) {
      toasts.push(error.message, 'error');
    }
  }
</script>

<section class="section-head">
  <div>
    <p class="eyebrow">Administración</p>
    <h1>Panel de control</h1>
  </div>
</section>

<section class="admin-layout">
  <div class="stack">
    <article class="panel">
      <p class="eyebrow">Productos</p>
      <h2>{selectedProduct ? 'Editar producto' : 'Crear producto'}</h2>
      <ProductForm
        product={selectedProduct}
        mode={selectedProduct ? 'edit' : 'create'}
        busy={productBusy}
        onSubmit={selectedProduct ? handleUpdateProduct : handleCreateProduct}
      />
      {#if selectedProduct}
        <button class="secondary" type="button" onclick={() => (selectedProduct = null)}>Cancelar edición</button>
      {/if}
    </article>

    <article class="panel">
      <p class="eyebrow">Usuarios</p>
      <h2>{selectedUser ? 'Editar usuario' : 'Crear usuario'}</h2>
      <UserForm
        user={selectedUser}
        busy={userBusy}
        onSubmit={selectedUser ? handleUpdateUser : handleCreateUser}
      />
      {#if selectedUser}
        <button class="secondary" type="button" onclick={() => (selectedUser = null)}>Cancelar edición</button>
      {/if}
    </article>
  </div>

  <div class="stack">
    <article class="panel">
      <p class="eyebrow">Catálogo actual</p>
      <h2>Productos registrados</h2>
      <div class="stack">
        {#each $products.items as product (product._id)}
          <ProductCard
            {product}
            isAdminView={true}
            onEdit={(value) => (selectedProduct = value)}
            onDelete={deleteProduct}
            onView={(value) => (viewedProduct = value)}
          />
        {/each}
      </div>
    </article>

    <article class="panel">
      <p class="eyebrow">Usuarios</p>
      <h2>Gestión de cuentas</h2>
      <div class="stack">
        {#each $users.items as user (user._id)}
          <div class="user-row">
            <div>
              <strong>{user.username}</strong>
              <p class="muted">{user.role}</p>
            </div>
            <div class="inline-actions">
              <button class="secondary" type="button" onclick={() => (selectedUser = user)}>Editar</button>
              <button class="danger" type="button" onclick={() => deleteUser(user)}>Eliminar</button>
            </div>
          </div>
        {/each}
      </div>
    </article>
  </div>
</section>

<ProductDetailModal product={viewedProduct} onClose={() => (viewedProduct = null)} />
