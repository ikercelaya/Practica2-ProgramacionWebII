import { derived, writable } from 'svelte/store';
import { api } from '../lib/api.js';

function createCartStore() {
  let snapshot = {
    items: [],
    loading: false
  };

  const { subscribe, set, update } = writable({
    items: [],
    loading: false
  });

  const syncSet = value => {
    snapshot = value;
    set(value);
  };

  const syncUpdate = recipe =>
    update(state => {
      const next = recipe(state);
      snapshot = next;
      return next;
    });

  return {
    subscribe,
    clear() {
      syncSet({ items: [], loading: false });
    },
    async load() {
      syncUpdate(state => ({ ...state, loading: true }));
      try {
        const items = await api.getCart();
        syncSet({ items, loading: false });
      } catch (error) {
        syncUpdate(state => ({ ...state, loading: false }));
        throw error;
      }
    },
    async add(productId) {
      syncUpdate(state => ({ ...state, loading: true }));
      try {
        const items = await api.addToCart(productId);
        syncSet({ items, loading: false });
      } catch (error) {
        syncUpdate(state => ({ ...state, loading: false }));
        throw error;
      }
    },
    async remove(productId) {
      syncUpdate(state => ({ ...state, loading: true }));
      try {
        const items = await api.removeFromCart(productId);
        syncSet({ items, loading: false });
      } catch (error) {
        syncUpdate(state => ({ ...state, loading: false }));
        throw error;
      }
    },
    async checkout() {
      const itemsToRemove = [...snapshot.items];
      syncUpdate(state => ({ ...state, loading: true }));
      try {
        for (const item of itemsToRemove) {
          await api.removeFromCart(item.productId._id);
        }
        syncSet({ items: [], loading: false });
      } catch (error) {
        syncUpdate(state => ({ ...state, loading: false }));
        throw error;
      }
    }
  };
}

export const cart = createCartStore();
export const cartCount = derived(cart, $cart =>
  $cart.items.reduce((total, item) => total + item.quantity, 0)
);
export const cartTotal = derived(cart, $cart =>
  $cart.items.reduce((total, item) => total + item.quantity * (item.productId?.precio || 0), 0)
);
