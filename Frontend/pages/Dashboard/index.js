const Storage = {
  get() {
    return JSON.parse(localStorage.getItem("dev.finances:transaction")) || [];
  },
  set(transactions) {
    localStorage.setItem(
      "dev.finances:transaction",
      JSON.stringify(transactions)
    );
  },
};

const Transaction = {
  all: Storage.get(),

  add(transaction) {
    //add transaction
    Transaction.all.push(transaction);
    App.reload();
  },
  remove(index) {
    Transaction.all.reverse().splice(index, 1);
    App.reload();
  },
  incomes() {
    // total incomes
    let income = 0;

    Transaction.all.forEach((transaction) => {
      if (transaction.amount > 0) {
        income += transaction.amount;
      }
    });
    return income;
  },
  expenses() {
    // total expenses
    let expense = 0;

    Transaction.all.forEach((transaction) => {
      if (transaction.amount < 0) {
        expense += transaction.amount;
      }
    });
    return expense;
  },
  total() {
    //total incomes + expenses
    return Transaction.incomes() + Transaction.expenses();
  },
};

const DOM = {
  transactionsContainer: document.querySelector("#data-table tbody"),

  addTransaction(transaction, index) {
    const tr = document.createElement("tr");
    tr.innerHTML = DOM.innerHTMLTransaction(transaction, index);
    tr.dataset.index = index;

    // adding transaction on html using the "DOM.innerHTMLTransaction" function
    DOM.transactionsContainer.appendChild(tr);
  },

  innerHTMLTransaction(transaction, index) {
    const CSSclass = transaction.amount > 0 ? "income" : "expense";

    const amount = Utils.formatCurrency(transaction.amount);

    const html = `
      <td class="description">${transaction.description}</td>
      <td class="${CSSclass}">${amount}</td>
      <td class="date">${transaction.date}</td>
      <td>
          <img onclick="Transaction.remove(${index})" src="./assets/x-circle.svg" class="remove-transaction" alt="Remover transação">
      </td>
      `;
    return html;
  },

  //update balance cards (incomes, expenses and total)
  updateBalance() {
    document.getElementById("incomeDisplay").innerHTML = Utils.formatCurrency(
      Transaction.incomes()
    );

    document.getElementById("expenseDisplay").innerHTML = Utils.formatCurrency(
      Transaction.expenses()
    );

    document.getElementById("totalDisplay").innerHTML = Utils.formatCurrency(
      Transaction.total()
    );
  },

  clearTransactions() {
    //clear transactions before update
    DOM.transactionsContainer.innerHTML = "";
  },
};

const Utils = {
  //formatting Form values
  formatAmount(value) {
    value = Number(value) * 100;

    //check if user add a - (minus sign) instead select "Income" and "Expense" Buttons
    if (value < 0) {
      value = -value;
    }
    if (Form.incomeOrExpense === "income") {
      value = value;
    } else {
      value = -value;
    }

    return value;
  },

  formatDate(date) {
    //date to user locale date
    date = date.toLocaleString();
    date = date.replaceAll("-", "/");
    return date;
  },

  formatCurrency(value) {
    //formatting value to user local currency
    value = Number(value) / 100;
    value = value.toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
    });

    return value;
  },
};

const Form = {
  description: document.querySelector("input#description"),
  amount: document.querySelector("input#amount"),
  date: document.querySelector("input#date"),
  incomeOrExpense: "",

  setIncome() {
    Form.incomeOrExpense = "income";
    document.querySelector("#incomeButton").classList.add("income");
    document.querySelector("#expenseButton").classList.remove("expense");
  },

  setExpense() {
    Form.incomeOrExpense = "expense";
    document.querySelector("#expenseButton").classList.add("expense");
    document.querySelector("#incomeButton").classList.remove("income");
  },

  getValues() {
    //get input (modal) values
    return {
      description: Form.description.value,
      amount: Form.amount.value,
      date: Form.date.value,
      incomeOrExpense: Form.incomeOrExpense,
    };
  },

  validateField() {
    const { description, amount, date, incomeOrExpense } = Form.getValues();

    if (
      description.trim() === "" ||
      amount.trim() === "" ||
      date.trim() === "" ||
      incomeOrExpense === ""
    ) {
      Swal.fire({
        icon: "warning",
        title: "Oops...",
        text: "Por favor, preencha todos os campos!",
      });
      throw new Error("Por favor, preencha todos os campos");
    }
  },

  formatValues() {
    let { description, amount, date, value } = Form.getValues();

    amount = Utils.formatAmount(amount);
    date = Utils.formatDate(date);

    return {
      description,
      amount,
      date,
    };
  },

  clearFields() {
    Form.description.value = "";
    Form.amount.value = "";
    Form.date.value = "";
    Form.value = "";
  },

  submit(event) {
    event.preventDefault();

    try {
      //verify fields before submit
      Form.validateField();
      const transaction = Form.formatValues();
      //salvar
      Transaction.add(transaction);
      //clear modal fields
      Form.clearFields();
      //close modal
      Modal.close();
    } catch (error) {
      console.log(error.message);
    }
  },
};