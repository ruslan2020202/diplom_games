const rows = 6;
const cols = 7;
let currentPlayer = 'X';
const board = [];

const createBoard = () => {
const boardElement = document.getElementById('board');
for (let i = 0; i < rows; i++) {
board[i] = Array.from({ length: cols }, () => '');
for (let j = 0; j < cols; j++) {
const cell = document.createElement('div');
cell.classList.add('cell');
cell.dataset.row = i;
cell.dataset.col = j;
cell.addEventListener('click', () => makeMove(j));
boardElement.appendChild(cell);
}
}
};

const makeMove = (col) => {
const row = findAvailableRow(col);
if (row === -1) return;
board[row][col] = currentPlayer;
renderBoard();
if (checkWin(row, col)) {
alert(`Player ${currentPlayer} wins!`);
location.reload();
}
currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
};

const findAvailableRow = (col) => {
for (let i = rows - 1; i >= 0; i--) {
if (board[i][col] === '') {
return i;
}
}
return -1;
};

const checkWin = (row, col) => {
return (
checkDirection(row, col, 1, 0) + checkDirection(row, col, -1, 0) >= 3 || // горизонталь
checkDirection(row, col, 0, 1) + checkDirection(row, col, 0, -1) >= 3 || // вертикаль
checkDirection(row, col, 1, 1) + checkDirection(row, col, -1, -1) >= 3 || // диагональ /
checkDirection(row, col, 1, -1) + checkDirection(row, col, -1, 1) >= 3 // диагональ \
);
};

const checkDirection = (row, col, dirRow, dirCol) => {
let count = 0;
let r = row + dirRow;
let c = col + dirCol;
while (r >= 0 && r < rows && c >= 0 && c < cols && board[r][c] === currentPlayer) {
count++;
r += dirRow;
c += dirCol;
}
return count;
};

const renderBoard = () => {
const cells = document.querySelectorAll('.cell');
cells.forEach(cell => {
const row = cell.dataset.row;
const col = cell.dataset.col;
cell.textContent = board[row][col];
});
};

createBoard();