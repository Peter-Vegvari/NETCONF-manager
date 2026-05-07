// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function getNestedValue(data: any, key: string): any {
  if (!data || typeof data !== "object") return undefined;
  const localName = key.includes(":") ? key.split(":")[1] : key;
  return data[key] ?? data[localName];
}
