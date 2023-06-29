'use strict';
const editButtons = document.querySelectorAll('.edit-movie-rating');

for (const button of editButtons) {
  button.addEventListener('click', () => {
    // first ask the user what they want the new rating to be
    const newScore = prompt('What is your new score for this movie?');
    const formInputs = {
      updated_score: newScore,
      rating_id: button.id,
    };

    // send a fetch request to the update_rating route
    fetch('/update_rating', {
      method: 'POST',
      body: JSON.stringify(formInputs),
      headers: {
        'Content-Type': 'application/json',
      },
    }).then((response) => {
      if (response.ok) {
        document.querySelector(`span.rating_num_${button.id}`).innerHTML = newScore;
      } else {
        alert('Failed to update rating.');
      }
    });
  });
}