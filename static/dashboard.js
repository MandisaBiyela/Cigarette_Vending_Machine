
var body = document.querySelector("body")
var dark_mode = document.querySelector("#toggle-dark")

dark_mode.addEventListener("click", () =>{
    console.log(body.classList)
    if ((body.classList[0] == undefined))
         body.classList.add("dark-mode")
    else 
         body.classList.remove("dark-mode")
})