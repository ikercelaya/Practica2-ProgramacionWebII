function decodeBase64Url(segment) {
  const normalized = segment.replace(/-/g, '+').replace(/_/g, '/');
  const padding = (4 - (normalized.length % 4)) % 4;
  return atob(normalized.padEnd(normalized.length + padding, '='));
}

export function parseToken(token) {
  try {
    const [, payload] = token.split('.');
    if (!payload) return null;
    return JSON.parse(decodeBase64Url(payload));
  } catch {
    return null;
  }
}
