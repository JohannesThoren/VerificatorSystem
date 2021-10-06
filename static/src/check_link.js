/*
 *   Copyright (c) 2021 Johannes Thorén
 *   All rights reserved.

 *   Permission is hereby granted, free of charge, to any person obtaining a copy
 *   of this software and associated documentation files (the "Software"), to deal
 *   in the Software without restriction, including without limitation the rights
 *   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 *   copies of the Software, and to permit persons to whom the Software is
 *   furnished to do so, subject to the following conditions:
 
 *   The above copyright notice and this permission notice shall be included in all
 *   copies or substantial portions of the Software.
 
 *   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 *   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 *   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 *   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 *   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 *   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 *   SOFTWARE.
 */

const steam_btn = document.getElementById("steam_link_btn")
const discord_btn = document.getElementById("discord_link_btn")
const steam_info = document.getElementById("steam_info")
const discord_info = document.getElementById("discord_info")

const current_address = document.URL

const settings_btn = document.getElementById("settings_btn")

if (steam_btn.href == current_address) {
      steam_info.innerText = "Account Linked"
      steam_info.className = "txt_ok center_text"
      steam_btn.innerHTML = "<i class=\"far fa-check-circle check\"></i>"
      steam_btn.removeAttribute("href")
      steam_btn.className = "center_item txt_ok"
      steam_btn.style.fontSize = "3em"

}

if (discord_btn.href == current_address) {
      discord_info.innerText = "Account Linked"
      discord_info.className = "txt_ok center_text"
      discord_btn.innerHTML = "<i class=\"far fa-check-circle check\"></i>"
      discord_btn.removeAttribute("href")
      discord_btn.className = "center_item txt_ok"
      discord_btn.style.fontSize = "3em"

}

if (discord_btn.href == "" && steam_btn.href == "") {
      settings_btn.className = "center_item button button_ok"
}
else {
      settings_btn.className = "hidden"
}