function populateTable(data) {
    const table = document.getElementById('data-table');
    const tbody = table.getElementsByTagName('tbody')[0];
    tbody.innerHTML = '';

    var x = {"Grocery": 0, "Travelling": 0, "Miscellaneous": 0, "House expenses": 0}

  
    for (const key in data) {
      if (data.hasOwnProperty(key)) {
        const payment = data[key].payment;
        const date = data[key].date;
        const user = data[key].user;
        const transactionCost = data[key].transaction_cost;
        const category = data[key].category;

        if (category == "Grocery"){
            x["Grocery"] = payment+x["Grocery"] + transactionCost

        }
        if (category == "Travelling"){
            x["Travelling"] = x["Travelling"] + payment + transactionCost
        }
        if (category == "Miscellaneous"){
            x["Miscellaneous"] = x["Miscellaneous"] + payment + transactionCost
        }
        if (category == "House expenses"){
            x["House expenses"] = x["House expenses"] + payment + transactionCost
        }
       
       
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>${category}</td>
        <td>${user}</td>
          <td>${payment}</td>
          <td>${transactionCost}</td>
          <td>${date}</td>
  
        `;
  
        tbody.appendChild(row);
      }
    }
    AddChart.update(x);
    console.log("Xx-values", x);
  }
  
  
  function populatecard(data){
    const card1=document.getElementById("incomeDisplay")
    card1.innerHTML= "Ksh. " + data['total_payments']
    
    const card2=document.getElementById("expenseDisplay")
    card2.innerHTML="Ksh. " + data["total_transactions"]
  
    const card3=document.getElementById("totalDisplay")
    card3.innerHTML= "Ksh. " + Math.round(data["total_expense"])
  }
  
  
  async function getDataFromAPI(url) {
      try {
     const response = await fetch(url);
  
     if (!response.ok) {
       throw new Error('Network response was not ok');
     }
  
     const data = await response.json();
     return data;
   } catch (error) {
     console.error('Error fetching data from the API:', error);
     return null;
   }
  }

  
  async function trans_method(apiUrl){
    getDataFromAPI(apiUrl) //fetch method to get data from api 
    .then(data => { // is a promise
    if (data) {
    console.log('Data from API:', data);
    populateTable(data["messages"])
    populatecard(data)
    // Process the data here
  }
  })
  .catch(error => {
  console.error('Error getting data from the API:', error);
  });
}
  
  trans_method('http://127.0.0.1:8000/')
  
  
  function getdate()
                  {
                    const datePicker = document.getElementById('datepicker');
                    const selectedDate = datePicker.value

                    const category = document.getElementById('expenseCategory');
                    const value = category.value

                    if (selectedDate && value ){
                        console.log("category:", value, "date:", selectedDate )

                        trans_method(`http://127.0.0.1:8000/?dateq=${selectedDate}&category=${value}`)
                    }
                    else if (selectedDate){
                        trans_method(`http://127.0.0.1:8000/?dateq=${selectedDate}`)
                        console.log("date:", selectedDate )

                    }
                    else if (value){
                        trans_method(`http://127.0.0.1:8000/?category=${value}`)
                        console.log("category:", value )
                    }
                  };

                  function trans_method(apiUrl) {
                    getDataFromAPI(apiUrl)
                      .then(data => {
                        if (data) {
                          console.log('Data from API:', data);
                          populateTable(data["messages"]);
                          populatecard(data);
                        }
                      })
                      .catch(error => {
                        console.error('Error getting data from the API:', error);
                      });
                  }
                  
                   function generatePDF() {
                    const datePicker = document.getElementById('datepicker');
                    const selectedDate = datePicker.value;
                
                    const category = document.getElementById('expenseCategory');
                    const value = category.value;
                
                    let apiUrl = 'http://127.0.0.1:8000/';
                
                    if (selectedDate && value) {
                        apiUrl += `?dateq=${selectedDate}&category=${value}`;
                    } else if (selectedDate) {
                        apiUrl += `?dateq=${selectedDate}`;
                    } else if (value) {
                        apiUrl += `?category=${value}`;
                    }
                
                    fetch(apiUrl, {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    })
                        .then(response => {
                            if (!response.ok) {
                                throw new Error('Network response was not ok');
                            }
                            return response.blob();
                        })
                        .then(blob => {
                            const link = document.createElement('a');
                            link.href = window.URL.createObjectURL(blob);
                            link.download = 'generated-pdf.pdf';
                            document.body.appendChild(link);
                            link.click();
                            document.body.removeChild(link);
                        })
                        .catch(error => {
                            console.error('Error generating PDF:', error);
                        });
                  };


                    // function generatePDF(data) {
                    //     const pdf = new jsPDF();
                        
                    //     // Add content to the PDF
                    //     pdf.text("Expense Report", 20, 10);
                        
                    //     const tableHeaders = ["Category", "User", "Payment", "Transaction Cost", "Date"];
                    //     const rows = [];
                        
                    //     for (const key in data) {
                    //         if (data.hasOwnProperty(key)) {
                    //             const category = data[key].category;
                    //             const user = data[key].user;
                    //             const payment = data[key].payment;
                    //             const transactionCost = data[key].transaction_cost;
                    //             const date = data[key].date;

                    //             rows.push([category, user, payment, transactionCost, date]);
                    //         }
                    //     }

                    //     pdf.autoTable({
                    //         head: [tableHeaders],
                    //         body: rows,
                    //     });

                    //     // Save the PDF
                    //     pdf.save("expense_report.pdf");
                    // }

                    // // Add this event listener to the button
                    // document.getElementById('generatePdfButton').addEventListener('click', function() {
                    //     generatePDF(data); // Pass your data object (x) to the function
                    // });


// DON'T TOUCH THIS CODE; I DONT KNOW HOW IT WORKS!


// ChartJS - doughnut chart - chart config
var ctx = document.getElementById("myChart");
var myDonutChart;

const AddChart = {
  Destroy() {
    if (myDonutChart) {
      myDonutChart.destroy();
    }
    this.update();
  },

  getData(d) {

    let data;
    console.log("inside chart", d)
    if (
        true
        //     var x = {"Grocery": 0, "Travelling": 0, "Miscellaneous": 0, "House expenses": 0}
    //   Transaction.incomes().toString() !== "0" ||
    //   Transaction.expenses().toString() !== "0"
    ) {
      data = {
        datasets: [
          {
            data: [d['Grocery'], d["Travelling"], d["Miscellaneous"], d["House expenses"]],
            backgroundColor: ["#28D39A", "#ff7782", "#7380EC", "#9a4eae"],
            usePointStyle: true,
          },
        ],
        labels: ["Grocery", "Travelling", "Miscellaneous", "House expenses"],
      };
    } else {
      data = {
        datasets: [
          {
            data: [100],
            backgroundColor: ["#bbb"],
            usePointStyle: true,
          },
        ],
        labels: ["No Transactions"],
      };
    }
    return data;
  },



  getOptions() {
    let options;
    if (
      Transaction.incomes().toString() === "0" &&
      Transaction.expenses().toString() === "0"
    ) {
      var style = getComputedStyle(document.body);
      const darkThemeTextColor = style.getPropertyValue("--color-info-dark");

      options = {
        tooltips: { enabled: false },
        hover: { mode: null },
        legend: {
          position: "bottom",
          usePointStyle: true,
          labels: {
            fontSize: 16,
            fontFamily: "Poppins, sans-serif",
            fontStyle: "500",
            fontColor: darkThemeTextColor,
            usePointStyle: true,
          },
        },
        responsive: true,
        maintainAspectRatio: false,
      };
    } else {
      var style = getComputedStyle(document.body);
      const darkThemeTextColor = style.getPropertyValue("--color-info-dark");

      options = {
        legend: {
          position: "bottom",
          usePointStyle: true,
          labels: {
            fontSize: 16,
            fontFamily: "Poppins, sans-serif",
            fontStyle: "500",
            fontColor: darkThemeTextColor,
            usePointStyle: true,
          },
          onHover: function (event, legendItem) {
            // There is only a legendItem when your mouse is positioned over one
            if (legendItem) {
              event.target.style.cursor = "pointer";
            }
          },
        },
        responsive: true,
        maintainAspectRatio: false,
      };
    }

    return options;
  },

  update(d) {
    let options = this.getOptions(); // ok
    let data = this.getData(d);


    myDonutChart = new Chart(ctx, {
      type: "doughnut",
      data: data,
      options: options,
    });
  },
};

const App = {
  init() {
  },
  reload() {
    myDonutChart.destroy();
    // AddChart.update();
    App.init();
  },
};

App.init();
// AddChart.update();