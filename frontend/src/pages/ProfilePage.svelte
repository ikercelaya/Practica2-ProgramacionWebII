<script>
  import { currentUser } from '../stores/auth.js';
  import { cartCount, cartTotal } from '../stores/cart.js';
  import { ordersCount } from '../stores/orders.js';

  const roleLabel = $derived($currentUser?.role === 'admin' ? 'Administrador' : 'Usuario');
</script>

<section class="section-head">
  <div>
    <p class="eyebrow">Perfil</p>
    <h1>Tu sesion actual</h1>
  </div>
</section>

<section class="grid two">
  <article class="panel">
    <p class="eyebrow">Cuenta</p>
    <h2>{$currentUser?.username}</h2>
    <p class="muted">Rol actual: {roleLabel}</p>
  </article>

  <article class="panel">
    <p class="eyebrow">Resumen</p>
    <h2>{$cartCount} productos en carrito</h2>
    <p class="muted">Importe actual: {$cartTotal.toFixed(2)} EUR</p>
    <p class="muted">Pedidos realizados: {$ordersCount}</p>
  </article>
</section>
