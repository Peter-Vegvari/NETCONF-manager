export function getNestedValue(
	data: Record<string, unknown> | undefined,
	key: string,
): unknown {
	if (!data || typeof data !== "object") return undefined;
	const localName = key.includes(":") ? key.split(":")[1] : key;
	return data[key] ?? data[localName];
}
