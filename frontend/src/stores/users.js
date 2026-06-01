import { writable } from 'svelte/store';
import { api } from '../lib/api.js';

function createUsersStore() {
  const { subscribe, set, update } = writable({
    items: [],
    loading: false
  });

  return {
    subscribe,
    async load() {
      update(state => ({ ...state, loading: true }));
      try {
        const items = await api.getUsers();
        set({ items, loading: false });
      } catch (error) {
        update(state => ({ ...state, loading: false }));
        throw error;
      }
    }
  };
}

export const users = createUsersStore();
