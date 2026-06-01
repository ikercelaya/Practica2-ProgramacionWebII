import { writable } from 'svelte/store';

function createToastStore() {
  const { subscribe, update } = writable([]);
  let id = 0;

  return {
    subscribe,
    push(message, type = 'info') {
      const toast = { id: ++id, message, type };
      update(items => [...items, toast]);
      setTimeout(() => {
        update(items => items.filter(item => item.id !== toast.id));
      }, 3200);
    }
  };
}

export const toasts = createToastStore();
