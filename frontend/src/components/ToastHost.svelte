<script>
  import { toasts } from '../lib/toast.js';
</script>

<div class="toast-host" aria-live="polite" aria-atomic="true">
  {#each $toasts as toast (toast.id)}
    <div class={`toast ${toast.type}`}>{toast.message}</div>
  {/each}
</div>
