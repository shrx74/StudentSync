export const USER_ID = 1

export async function request(path, options = {}) {
  const response = await fetch(`/users/${USER_ID}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.error || 'Something went wrong')
  }

  return data
}
