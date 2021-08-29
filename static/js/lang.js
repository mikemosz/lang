$(document).ready(function() {
	$('.answer-btn').click(function(e) {
		e.preventDefault();

		$(this).hide();
		$(this).next('.answer-text').show();
	});

	$('.answer-text').click(function(e) {
		$(this).text('Loading...');
		console.log('here');

		$.get('/?json=1', function(data) {
			$('.answer-text').hide();
			$('.answer-btn').show();

			$('.prompt-text').text(data['prompt']);
			$('.answer-text').text(data['answer']);
		}, 'json');
	});
});