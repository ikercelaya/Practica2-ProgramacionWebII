import { writable } from 'svelte/store';
import { api } from '../lib/api.js';

function createProductsStore() {
  const { subscribe, set, update } = writable({
    items: [],
    loading: false,
    search: ''
  });

  return {
    subscribe,
    async load(search = '') {
      update(state => ({ ...state, loading: true, search }));
      try {
        const items = await api.getProducts(search);
        set({ items, loading: false, search });
      } catch (error) {
        update(state => ({ ...state, loading: false }));
        throw error;
      }
    }
  };
}

export const products = createProductsStore();
