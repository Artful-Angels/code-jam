const iconUrl = `${window.location.origin}/apple-touch-icon.png`

export function sendNotification(title, body, tag) {
  if (!(window.Notification) || Notification.permission === "denied") return
  if (document.hasFocus()) return
  if (Notification.permission === "default") {
    return Notification.requestPermission().then((result) => {
      if (result !== "granted") return
      new Notification(title, {
        body: body,
        tag: tag,
        icon: iconUrl,
      })
    })
  } else {
    new Notification(title, {
      body: body,
      tag: tag,
      icon: iconUrl,
    })
  }
}
