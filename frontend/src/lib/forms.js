export function readFormData(formElement) {
  const formData = new FormData(formElement);
  return Object.fromEntries(formData.entries());
}
