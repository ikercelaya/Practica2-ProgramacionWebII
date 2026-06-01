<script>
  import { onMount } from 'svelte';
  import Layout from './components/Layout.svelte';
  import ToastHost from './components/ToastHost.svelte';
  import HomePage from './pages/HomePage.svelte';
  import LoginPage from './pages/LoginPage.svelte';
  import RegisterPage from './pages/RegisterPage.svelte';
  import CatalogPage from './pages/CatalogPage.svelte';
  import ProfilePage from './pages/ProfilePage.svelte';
  import OrdersPage from './pages/OrdersPage.svelte';
  import CartPage from './pages/CartPage.svelte';
  import AdminPage from './pages/AdminPage.svelte';
  import NotFoundPage from './pages/NotFoundPage.svelte';
  import { currentPath, router } from './lib/router.js';
  import { cart } from './stores/cart.js';
  import { auth, isAuthenticated, isAdmin } from './stores/auth.js';

  const protectedRoutes = new Set(['/perfil', '/pedidos', '/carrito', '/admin']);

  const Page = $derived.by(() => {
    if ($currentPath === '/') return HomePage;
    if ($currentPath === '/login') return LoginPage;
    if ($currentPath === '/register') return RegisterPage;
    if ($currentPath === '/catalogo') return CatalogPage;
    if ($currentPath === '/perfil') return ProfilePage;
    if ($currentPath === '/pedidos') return OrdersPage;
    if ($currentPath === '/carrito') return CartPage;
    if ($currentPath === '/admin') return AdminPage;
    return NotFoundPage;
  });

  onMount(async () => {
    if ($isAuthenticated) {
      try {
        await cart.load();
      } catch {
        auth.reset();
        cart.clear();
        router.replace('/login');
      }
    }
  });

  $effect(() => {
    if (protectedRoutes.has($currentPath) && !$isAuthenticated) {
      router.replace('/login');
      return;
    }

    if ($currentPath === '/admin' && $isAuthenticated && !$isAdmin) {
      router.replace('/catalogo');
    }
  });
</script>

<Layout>
  <Page />
</Layout>

<ToastHost />
