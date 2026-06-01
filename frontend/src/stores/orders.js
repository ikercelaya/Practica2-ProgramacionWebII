import { derived, writable } from 'svelte/store';
import { currentUser } from './auth.js';

const STORAGE_KEY = 'orders_by_user';

function readOrdersMap() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
  } catch {
    return {};
  }
}

function writeOrdersMap(value) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(value));
}

function getUserKey(user) {
  return user?.id || user?.username || 'guest';
}

function createOrdersStore() {
  const { subscribe, set } = writable({ items: [] });

  return {
    subscribe,
    loadForUser(user) {
      const ordersMap = readOrdersMap();
      const userKey = getUserKey(user);
      set({ items: ordersMap[userKey] || [] });
    },
    createOrder({ user, items, total }) {
      const ordersMap = readOrdersMap();
      const userKey = getUserKey(user);
      const nextOrder = {
        id: `PED-${Date.now()}`,
        createdAt: new Date().toISOString(),
        total,
        items: items.map(item => ({
          productId: item.productId?._id,
          nombre: item.productId?.nombre || 'Producto',
          precio: item.productId?.precio || 0,
          quantity: item.quantity
        }))
      };

      const nextItems = [nextOrder, ...(ordersMap[userKey] || [])];
      ordersMap[userKey] = nextItems;
      writeOrdersMap(ordersMap);
      set({ items: nextItems });
      return nextOrder;
    }
  };
}

export const orders = createOrdersStore();
export const ordersCount = derived(orders, $orders => $orders.items.length);

currentUser.subscribe(user => {
  orders.loadForUser(user);
});
