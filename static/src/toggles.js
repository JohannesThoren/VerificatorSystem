const togg_1 = document.getElementById("togg_1")
const togg_2 = document.getElementById("togg_2")
const togg_3 = document.getElementById("togg_3")
const togg_4 = document.getElementById("togg_4")

if (togg_1.innerText == "False") {
    togg_1.className = "txt_warning"
} else {
    togg_1.className = "txt_ok"
}
if (togg_2.innerText == "False") {
    togg_2.className = "txt_warning"
}  else {
    togg_2.className = "txt_ok"
}
if (togg_3.innerText == "False") {
    togg_3.className = "txt_warning"
}  else {
    togg_3.className = "txt_ok"
}
if (togg_4.innerText == "False") {
    togg_4.className = "txt_warning"
}  else {
    togg_4.className = "txt_ok"
}