<script>
  import { auth } from '../stores/auth.js';
  import { router } from '../lib/router.js';
  import { toasts } from '../lib/toast.js';
  import { readFormData } from '../lib/forms.js';

  let loading = $state(false);

  async function submit(event) {
    event.preventDefault();
    const values = readFormData(event.currentTarget);
    loading = true;

    try {
      await auth.register(values);
      toasts.push('Usuario registrado correctamente. Ya puedes iniciar sesión.', 'success');
      router.go('/login');
    } catch (error) {
      toasts.push(error.message, 'error');
    } finally {
      loading = false;
    }
  }
</script>

<section class="auth-wrap">
  <div class="panel auth-card">
    <p class="eyebrow">Alta</p>
    <h1>Crear cuenta</h1>
    <p class="muted">El backend registra usuarios nuevos con rol user por defecto.</p>

    <form class="form-grid" onsubmit={submit}>
      <div class="full">
        <label for="username">Usuario</label>
        <input id="username" name="username" type="text" required />
      </div>

      <div class="full">
        <label for="password">Contraseña</label>
        <input id="password" name="password" type="password" minlength="6" required />
      </div>

      <div class="full">
        <button class="primary" type="submit" disabled={loading}>
          {loading ? 'Registrando...' : 'Crear cuenta'}
        </button>
      </div>
    </form>
  </div>
</section>
