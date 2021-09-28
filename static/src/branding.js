const title = document.getElementById("branding-title")
const icon = document.getElementById("branding-icon")
const info = document.getElementById("branding-info")

fetch("/branding")
.then(resp => resp.json())
.then(data => {
    title.innerText = data["title"]
    icon.src = data["icon"]
    info.innerText = data["info"]
})