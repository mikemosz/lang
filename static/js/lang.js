$(document).ready(function() {
	$('.answer-btn').click(function(e) {
		e.preventDefault();

		$(this).closest('.answer').addClass('revealed');
	});

	$('.answer-text').click(function(e) {
		$(this).text('Loading...');
		console.log('here');

		$.get('/?json=1', function(data) {
			$('.prompt-text').text(data['prompt']);
			$('.answer-text').text(data['answer']);
			$('.answer').removeClass('revealed');
		}, 'json');
	});
});