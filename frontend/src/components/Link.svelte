<script>
  import { router } from '../lib/router.js';

  let { href = '/', className = '', children } = $props();

  function handleClick(event) {
    if (event.defaultPrevented || event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0) {
      return;
    }

    event.preventDefault();
    router.go(href);
  }
</script>

<a href={href} class={className} onclick={handleClick}>
  {@render children?.()}
</a>
