export async function apiGet(path: string) {
  const response = await fetch(path, {
    headers: { Accept: "application/json" },
    credentials: "include",
  })

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`)
  }

  return response.json()
}