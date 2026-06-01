<script>
  import { readFormData } from '../lib/forms.js';

  let { user = null, busy = false, onSubmit } = $props();
  let role = $state('user');

  $effect(() => {
    role = user?.role || 'user';
  });

  function submit(event) {
    event.preventDefault();
    onSubmit?.(readFormData(event.currentTarget));
  }
</script>

<form class="panel form-grid" onsubmit={submit}>
  <div>
    <label for="username">Usuario</label>
    <input id="username" name="username" type="text" required value={user?.username || ''} />
  </div>

  <div>
    <label for="role">Rol</label>
    <select id="role" name="role" bind:value={role}>
      <option value="user">user</option>
      <option value="admin">admin</option>
    </select>
  </div>

  <div class="full">
    <label for="password">Contraseña {user ? '(opcional)' : ''}</label>
    <input id="password" name="password" type="password" minlength="6" required={!user} />
  </div>

  <div class="full">
    <button class="primary" type="submit" disabled={busy}>
      {busy ? 'Guardando...' : user ? 'Actualizar usuario' : 'Crear usuario'}
    </button>
  </div>
</form>
