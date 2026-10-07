document.querySelectorAll('.accordion-header').forEach(function(btn) {
btn.addEventListener('click', function() {
var expanded = this.getAttribute('aria-expanded') === 'true';
this.setAttribute('aria-expanded', String(!expanded));
var body = this.nextElementSibling;
if (expanded) {
body.style.maxHeight = null;
} else {
body.style.maxHeight = body.scrollHeight + 'px';
}
});
});