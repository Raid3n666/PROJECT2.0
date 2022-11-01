const button = document.getElementById('sort');
button.addEventListener('click', sortByDate);

function convertDate(d) {
    var p = d.split("/");
    return +(p[2]+p[1]+p[0]);
  }
  
  function sortByDate() {
    var tbody = document.getElementsByTagName("tbody")[0];
    // get trs as array for ease of use
    var rows = [].slice.call(tbody.querySelectorAll("tr"));
    
    rows.sort(function(a,b) {
      return convertDate(a.cells[3].innerHTML) - convertDate(b.cells[3].innerHTML);
    });
    
    rows.forEach(function(v) {
      tbody.appendChild(v); // note that .appendChild() *moves* elements
    });
    
    button.textContent = 'Unsort'
    button.onclick = () => {location.reload()}
  }



