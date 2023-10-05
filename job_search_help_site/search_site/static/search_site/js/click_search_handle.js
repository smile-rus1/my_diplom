const searchForm = document.getElementById('search-form');
const searchInput = document.querySelector('input[name="resume"]');
const clickableStrings = document.querySelectorAll('.clickable-string');

// Функция, которая добавляет текст из кликаемой строки в поисковую строку
function handleClickableStringClick(event) {
    const clickedString = event.target.textContent;
    searchInput.value = clickedString;
    searchForm.submit();
}

// Добавляем обработчик события клика для каждой кликаемой строки
clickableStrings.forEach(string => {
    string.addEventListener('click', handleClickableStringClick);
});