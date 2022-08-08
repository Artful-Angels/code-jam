const iconUrl = `${window.location.origin}/apple-touch-icon.png`

export function sendNotification(title, body, tag) {
  if (!(window.Notification) || Notification.permission === "denied") return false
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
    console.log("sending!")
    new Notification(title, {
      body: body,
      tag: tag,
      icon: iconUrl,
    })
  }
}
