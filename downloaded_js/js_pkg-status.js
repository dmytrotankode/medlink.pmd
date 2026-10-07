(function () {
document.querySelectorAll('.pkg-sum').forEach(function (el) {
el.addEventListener('click', function () {
this.parentElement.classList.toggle('is-open');
});
});
document.querySelectorAll('.show-more-history').forEach(function (btn) {
btn.addEventListener('click', function (e) {
e.stopPropagation();
var b = document.getElementById('extraUpdates');
b.classList.toggle('show');
this.textContent = b.classList.contains('show')
? 'Приховати старі записи'
: 'Показати всю історію';
});
});
})();