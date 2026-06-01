<script>
  import Link from './Link.svelte';
  import { router, currentPath } from '../lib/router.js';
  import { auth, currentUser, isAuthenticated, isAdmin } from '../stores/auth.js';
  import { cart, cartCount } from '../stores/cart.js';

  let { children } = $props();

  const links = [
    { href: '/', label: 'Inicio' },
    { href: '/catalogo', label: 'Catalogo' },
    { href: '/perfil', label: 'Perfil', auth: true },
    { href: '/pedidos', label: 'Pedidos', auth: true },
    { href: '/carrito', label: 'Carrito', auth: true },
    { href: '/admin', label: 'Administracion', admin: true }
  ];

  function logout() {
    auth.logout();
    cart.clear();
    router.go('/login');
  }
</script>

<div class="shell">
  <header class="topbar">
    <div>
      <p class="eyebrow">Practica 1</p>
      <Link href="/" className="brand">PW2 Shop</Link>
    </div>

    <nav class="nav">
      {#each links as link}
        {#if (!link.auth || $isAuthenticated) && (!link.admin || $isAdmin)}
          <Link href={link.href} className={$currentPath === link.href ? 'nav-link active' : 'nav-link'}>
            {link.label}
          </Link>
        {/if}
      {/each}
    </nav>

    <div class="actions">
      {#if $isAuthenticated}
        <span class="badge">{$currentUser?.username} · {$currentUser?.role}</span>
        <Link href="/carrito" className="cart-chip">Carrito ({$cartCount})</Link>
        <button class="secondary" type="button" onclick={logout}>Salir</button>
      {:else}
        <Link href="/login" className="secondary-link">Entrar</Link>
        <Link href="/register" className="primary-link">Crear cuenta</Link>
      {/if}
    </div>
  </header>

  <main class="page">
    {@render children?.()}
  </main>
</div>
