import { derived, writable } from 'svelte/store';
import { api } from '../lib/api.js';
import { parseToken } from '../lib/jwt.js';

function createAuthStore() {
  const initialToken = localStorage.getItem('token');
  const initialUser = initialToken ? parseToken(initialToken) : null;

  const { subscribe, set, update } = writable({
    token: initialToken,
    user: initialUser,
    loading: false
  });

  return {
    subscribe,
    async login(credentials) {
      update(state => ({ ...state, loading: true }));
      try {
        const { token } = await api.login(credentials);
        const user = parseToken(token);
        localStorage.setItem('token', token);
        set({ token, user, loading: false });
        return user;
      } catch (error) {
        update(state => ({ ...state, loading: false }));
        throw error;
      }
    },
    register(payload) {
      return api.register(payload);
    },
    logout() {
      localStorage.removeItem('token');
      set({ token: null, user: null, loading: false });
    },
    reset() {
      localStorage.removeItem('token');
      set({ token: null, user: null, loading: false });
    }
  };
}

export const auth = createAuthStore();
export const currentUser = derived(auth, $auth => $auth.user);
export const isAuthenticated = derived(auth, $auth => Boolean($auth.token));
export const isAdmin = derived(auth, $auth => $auth.user?.role === 'admin');
