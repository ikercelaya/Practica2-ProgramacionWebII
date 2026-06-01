<script>
  import Link from './Link.svelte';
</script>

<section class="hero">
  <div class="hero-copy">
    <p class="eyebrow">Svelte 5 + API Express</p>
    <h1>Tienda completa con autenticación, carrito y administración</h1>
    <p>
      Frontend SPA conectado a tu backend real, con gestión de sesión mediante JWT,
      navegación protegida y panel de control por roles.
    </p>
    <div class="hero-actions">
      <Link href="/catalogo" className="primary-link">Ver catálogo</Link>
      <Link href="/login" className="secondary-link">Iniciar sesión</Link>
    </div>
  </div>

  <div class="hero-card">
    <div class="metric">
      <span>JWT</span>
      <strong>Sesión persistente</strong>
    </div>
    <div class="metric">
      <span>Roles</span>
      <strong>admin / user</strong>
    </div>
    <div class="metric">
      <span>Estado</span>
      <strong>Stores globales</strong>
    </div>
  </div>
</section>
