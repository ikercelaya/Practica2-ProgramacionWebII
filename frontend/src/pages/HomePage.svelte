<script>
  import Hero from '../components/Hero.svelte';
  import Link from '../components/Link.svelte';
</script>

<Hero />

<section class="grid two">
  <article class="panel">
    <p class="eyebrow">Usuario</p>
    <h2>Experiencia de compra</h2>
    <p>Consulta productos, busca por nombre, inicia sesión y gestiona tu carrito conectado a MongoDB.</p>
    <Link href="/catalogo" className="text-link">Ir al catálogo</Link>
  </article>

  <article class="panel">
    <p class="eyebrow">Administrador</p>
    <h2>Gestión completa</h2>
    <p>Crea, edita y elimina productos, además de administrar usuarios según el rol recibido en el JWT.</p>
    <Link href="/admin" className="text-link">Abrir administración</Link>
  </article>
</section>
