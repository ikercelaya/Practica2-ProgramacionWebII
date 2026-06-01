<script>
  import { auth } from '../stores/auth.js';
  import { cart } from '../stores/cart.js';
  import { router } from '../lib/router.js';
  import { toasts } from '../lib/toast.js';
  import { readFormData } from '../lib/forms.js';

  let loading = $state(false);

  async function submit(event) {
    event.preventDefault();
    const values = readFormData(event.currentTarget);
    loading = true;

    try {
      const user = await auth.login(values);
      await cart.load();
      toasts.push(`Sesión iniciada como ${user.username}`, 'success');
      router.go(user.role === 'admin' ? '/admin' : '/catalogo');
    } catch (error) {
      toasts.push(error.message, 'error');
    } finally {
      loading = false;
    }
  }
</script>

<section class="auth-wrap">
  <div class="panel auth-card">
    <p class="eyebrow">Acceso</p>
    <h1>Iniciar sesión</h1>
    <p class="muted">Usa por ejemplo admin / admin123 o user / user123 si ejecutas el seed del backend.</p>

    <form class="form-grid" onsubmit={submit}>
      <div class="full">
        <label for="username">Usuario</label>
        <input id="username" name="username" type="text" required />
      </div>

      <div class="full">
        <label for="password">Contraseña</label>
        <input id="password" name="password" type="password" required />
      </div>

      <div class="full">
        <button class="primary" type="submit" disabled={loading}>
          {loading ? 'Entrando...' : 'Entrar'}
        </button>
      </div>
    </form>
  </div>
</section>
