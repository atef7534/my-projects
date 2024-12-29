// ----------------------------------------------- 
// --------------- header background ------------- 
// ----------------------------------------------- 

let cols = document.getElementsByClassName("col");
let header = document.querySelector(".header");
let titlePrayers = document.querySelector(".title-prayers")
let thead = document.querySelector(".tt");
let btns = document.querySelectorAll(".btn");
let color;
if (localStorage.color)
  color = localStorage.color;
else
{
  localStorage.color = "#800080";
  color = "#800080";
}
setColor();

function setColor()
{
    header.style.backgroundColor = color; 
    if (titlePrayers) titlePrayers.style.color = color;
    if (thead) thead.style.backgroundColor = color;
    for (let j = 0; j < btns.length; j++)
    {
      btns[j].style.color = color;
      btns[j].style.backgroundColor = "#FFF";
      btns[j].style.borderColor = color;
    }
}

setColor();
for (let i = 0; i < cols.length; i++)
{
  cols[i].addEventListener("click", function () {
    localStorage.color = `${cols[i].dataset.col}`;
    color = localStorage.color;
    setColor();
  });
}

