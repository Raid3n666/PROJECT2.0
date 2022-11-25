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


function showFormBlock() {
  const button =  document.getElementsByClassName('add-form')[0]
  button.style.display = 'none'
  const div = document.getElementsByClassName('form')[0]
  div.style.display = 'block'
}

function closeForm() {
  const div = document.getElementsByClassName('form')[0]
  div.style.display = 'none'
  const button =  document.getElementsByClassName('add-form')[0]
  button.style.display = 'inline'

}

function searchTable(){
  // Declare variables 
  var input, filter, table, tr, td, i;
  input = document.getElementById("searchInput");
  filter = input.value.toUpperCase();
  table = document.getElementsByTagName("table")[0];
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td") ; 
    for(j=0 ; j<td.length ; j++)
    {
      let tdata = td[j] ;
      if (tdata) {
        if (tdata.innerHTML.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
          break ; 
        } else {
          tr[i].style.display = "none";
        }
      } 
    }
  }
}
