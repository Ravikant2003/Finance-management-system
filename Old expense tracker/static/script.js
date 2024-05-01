const totalExpensesElement = document.getElementById('total-expenses');
const expenseLimitInput = document.getElementById('expense-limit-input');
const expenseLimitWarning = document.getElementById('expense-limit-warning');
const expenseNameElement = document.getElementById('expense-name');
const expenseAmountElement = document.getElementById('expense-amount');
const expenseCategoryElement = document.getElementById('expense-category');
const addExpenseButton = document.getElementById('add-expense');
const expenseListElement = document.getElementById('expense-list');

let totalExpenses = 0;
let expenses = [];
let expenseLimit = null;

function updateTotalExpenses() {
    totalExpensesElement.textContent = totalExpenses.toFixed(2);
    checkExpenseLimit();
}

function checkExpenseLimit() {
    if (expenseLimit !== null && totalExpenses > expenseLimit) {
        expenseLimitWarning.textContent = "Expense Limit Reached";
        expenseLimitWarning.classList.add('warning');
    } else {
        expenseLimitWarning.textContent = "";
        expenseLimitWarning.classList.remove('warning');
    }
}

function updateExpenseList() {
    expenseListElement.innerHTML = '';
    expenses.forEach((expense, index) => {
        const expenseItem = document.createElement('div');
        expenseItem.classList.add('expense-item');
        expenseItem.innerHTML = `
            <span>${expense.name}</span>
            <span>$${expense.amount.toFixed(2)}</span>
            <span>${expense.category}</span>
            <span class="edit-remove">
                <button class="edit-btn" onclick="editExpense(${index})">Edit</button>
                <button class="remove-btn" onclick="removeExpense(${index})">Remove</button>
            </span>
        `;
        expenseListElement.appendChild(expenseItem);
    });
}

function addExpense() {
    const name = expenseNameElement.value;
    const amount = parseFloat(expenseAmountElement.value);
    const category = expenseCategoryElement.value;

    if (name && !isNaN(amount) && category) {
        totalExpenses += amount;
        expenses.push({ name, amount, category });

        updateTotalExpenses();
        updateExpenseList();

        expenseNameElement.value = '';
        expenseAmountElement.value = '';
        expenseCategoryElement.value = 'groceries';
    }
}

function editExpense(index) {
    const newAmount = parseFloat(prompt("Enter the new amount:"));
    if (!isNaN(newAmount)) {
        const oldAmount = expenses[index].amount;
        totalExpenses += newAmount - oldAmount;
        expenses[index].amount = newAmount;
        updateTotalExpenses();
        updateExpenseList();
    }
}

function removeExpense(index) {
    const removedAmount = expenses[index].amount;
    totalExpenses -= removedAmount;
    expenses.splice(index, 1);
    updateTotalExpenses();
    updateExpenseList();
}

expenseLimitInput.addEventListener('input', function () {
    expenseLimit = parseFloat(expenseLimitInput.value);
    checkExpenseLimit();
});

addExpenseButton.addEventListener('click', addExpense);