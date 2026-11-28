export function money(amount) {
  return `$${Number(amount).toFixed(2)}`
}

export function dateTime(value) {
  const date = new Date(value)
  const day = date.toLocaleDateString('en-CA')
  const time = date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
  return `${day}, ${time}`
}

export function clockTime(value) {
  return new Date(value).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}
