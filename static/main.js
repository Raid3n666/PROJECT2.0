const button = document.getElementById('sort');
button.addEventListener('click', sortByDate);
const tbody = document.getElementsByTagName("tbody")[0];
const rows = [].slice.call(tbody.querySelectorAll("tr"));

function convertDate(d) {
    var p = d.split("/");
    return +(p[2]+p[1]+p[0]);
  }

  function sortByDate() {    
    rows.sort(function(a,b) {
      return convertDate(a.cells[3].innerHTML) - convertDate(b.cells[3].innerHTML);
    });
    
    rows.forEach(function(v) {
      tbody.appendChild(v); // note that .appendChild() *moves* elements
    });
    
    button.textContent = 'Unsort'
    button.onclick = () => {location.reload()}
  }

// turn 0₪ to Free
for (i in rows){
  if (i > 0){
    if (rows[i].getElementsByClassName('price')[0].textContent === '0₪'){
      rows[i].getElementsByClassName('price')[0].textContent = 'Free'
    }
  }
}


