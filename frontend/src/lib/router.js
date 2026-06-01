import { writable, derived, get } from 'svelte/store';

const normalize = path => {
  if (!path) return '/';
  const cleaned = path.startsWith('/') ? path : `/${path}`;
  return cleaned.length > 1 ? cleaned.replace(/\/+$/, '') : cleaned;
};

function createRouter() {
  const current = writable(normalize(window.location.pathname));

  const sync = () => current.set(normalize(window.location.pathname));
  window.addEventListener('popstate', sync);

  return {
    subscribe: current.subscribe,
    go(path) {
      const next = normalize(path);
      if (get(current) !== next) {
        window.history.pushState({}, '', next);
      }
      current.set(next);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    replace(path) {
      const next = normalize(path);
      window.history.replaceState({}, '', next);
      current.set(next);
    }
  };
}

export const router = createRouter();
export const currentPath = derived(router, $router => $router);
