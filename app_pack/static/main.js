/* ---------   Calneder js ---------- */
const monthYearElement = document.getElementById("monthYear");
const datesElement = document.getElementById("dates");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");


let currentDate = new Date();

const updateCalendar = () => {
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth();

    const firstDay= new Date(currentYear, currentMonth, 0);
    const lastDay = new Date(currentYear, currentMonth+1, 0);
    const totalDays = lastDay.getDate();
    const firstDayIndex = firstDay.getDay();
    const lastDayIndex = lastDay.getDay();

    const monthYearString = currentDate.toLocaleDateString('default', {month: 'long', year: 'numeric'});
    monthYearElement.textContent = monthYearString;

    let datesHTML = "";

    for (let i = firstDayIndex; i>0; i--) {
        const prevDate = new Date(currentYear, currentMonth, 0 - i + 1);
        console.log(firstDayIndex);
        datesHTML += `<div class="date inactive">${prevDate.getDate()}</div>`;
    }

    for (let i = 1; i <= totalDays; i++) {
        const date = new Date(currentYear, currentMonth, i);
        const activeClass = date.toDateString() === new Date().toDateString() ? 'active' : '';
        datesHTML += `<div class="date ${activeClass}">${i}</div>`;
    }

    for (let i = 1; i<= 7 - lastDayIndex; i++) {
        const nextDate = new Date(currentYear, currentMonth + 1, i);
        datesHTML += `<div class="date inactive">${nextDate.getDate()}</div>`;
    }

    datesElement.innerHTML = datesHTML;
}

prevBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    updateCalendar();
})

nextBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    updateCalendar();
})

updateCalendar();

/* ------------ DropDown ----------- */
document.body.addEventListener('click', function(event) {
    var dropdown = document.getElementById("dropdownContent");
    var user = document.querySelector(".user");

    // Check if the clicked element is not the user element or the dropdown content
    if (!user.contains(event.target) && !dropdown.contains(event.target)) {
        dropdown.style.display = "none"; // Close the dropdown
    }
});

function toggleDropdown() {
    var dropdown = document.getElementById("dropdownContent");
    if (dropdown.style.display === "block") {
        dropdown.style.display = "none";
    } else {
        dropdown.style.display = "block";
    }
}


/* ----------- chart js -------------- */


var options = {
    series: [{
    name: '2024',
    data: [31, 40, 28, 51, 42, 109, 100]
  }, {
    name: '2023',
    data: [11, 32, 45, 32, 34, 52, 41]
  }],
    chart: {
    height: 500,
    type: 'area'
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    curve: 'smooth'
  },
  xaxis: {
    type: 'datetime',
    categories: ["2018-09-19T00:00:00.000Z", "2018-09-19T01:30:00.000Z", "2018-09-19T02:30:00.000Z", "2018-09-19T03:30:00.000Z", "2018-09-19T04:30:00.000Z", "2018-09-19T05:30:00.000Z", "2018-09-19T06:30:00.000Z"]
  },
  tooltip: {
    x: {
      format: 'dd/MM/yy HH:mm'
    },
  },
  title: {
    text: 'Activité Recentes',
    align: 'left',
    style: {
      fontSize: '20px'
    }
  },
  };

  var chart = new ApexCharts(document.querySelector("#chart"), options);
  chart.render();