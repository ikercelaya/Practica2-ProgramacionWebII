import { API_URL } from '../config.js';

async function request(path, options = {}) {
  const headers = new Headers(options.headers || {});
  const token = options.token || localStorage.getItem('token');

  if (!(options.body instanceof FormData) && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers
  });

  const isJson = response.headers.get('content-type')?.includes('application/json');
  const data = isJson ? await response.json() : await response.text();

  if (!response.ok) {
    const message =
      (typeof data === 'object' && (data.error || data.message)) ||
      response.statusText ||
      'Error inesperado';
    throw new Error(message);
  }

  return data;
}

export const api = {
  login(credentials) {
    return request('/login', { method: 'POST', body: JSON.stringify(credentials) });
  },
  register(payload) {
    return request('/register', { method: 'POST', body: JSON.stringify(payload) });
  },
  getProducts(search = '') {
    const params = search ? `?name=${encodeURIComponent(search)}` : '';
    return request(`/productos${params}`);
  },
  createProduct(payload) {
    return request('/productos', { method: 'POST', body: payload });
  },
  updateProduct(id, payload) {
    return request(`/productos/${id}`, { method: 'PUT', body: JSON.stringify(payload) });
  },
  deleteProduct(id) {
    return request(`/productos/${id}`, { method: 'DELETE' });
  },
  getCart() {
    return request('/cart');
  },
  addToCart(productId) {
    return request('/cart/add', {
      method: 'POST',
      body: JSON.stringify({ productId })
    });
  },
  removeFromCart(productId) {
    return request(`/cart/${productId}`, { method: 'DELETE' });
  },
  getUsers() {
    return request('/users');
  },
  createUser(payload) {
    return request('/users', { method: 'POST', body: JSON.stringify(payload) });
  },
  updateUser(id, payload) {
    return request(`/users/${id}`, { method: 'PUT', body: JSON.stringify(payload) });
  },
  deleteUser(id) {
    return request(`/users/${id}`, { method: 'DELETE' });
  }
};
