var scroller = document.querySelector("#scroller");
var template = document.querySelector('#image_template');
var sentinel = document.querySelector('#sentinel');

var cursor = "start";
function loadItems() {
	if (cursor != 'finished') {
		fetch(`/load?c=${cursor}`).then((response) => {
			response.json().then((data) => {
				cursor = data[0];
				if (data[1].length == 0) {
					return;
				}

				for (var i = 0; i < data[1].length; i++) {
					let template_clone = template.content.cloneNode(true);
					template_clone.querySelector("#image").src = 'https://storage.googleapis.com/image-colorization-280016-images/grayscale/' + data[1][i].path;
					template_clone.querySelector("#image").onmouseover = function () {
						this.src = this.src.replace('grayscale', 'colored');
					};
					template_clone.querySelector("#image").onmouseout = function () {
						this.src = this.src.replace('colored', 'grayscale');
					};

					scroller.appendChild(template_clone);
				}
			});
		});
	}
}

var intersectionObserver = new IntersectionObserver(entries => {
	if (entries[0].intersectionRatio <= 0) {
		return;
	}
	loadItems();
});

intersectionObserver.observe(sentinel);