

    // Getting the logic for editing
    document.addEventListener("DOMContentLoaded", () => {
        document.querySelectorAll('.list-group-item').forEach(div => {
            const button = div.querySelector('#edit_button');
            if (button) {
                button.onclick = () => {
                    div.querySelector('#edit_box').value = div.querySelector('#entry').innerHTML;
                    div.querySelector('#edit_form').style.display = 'block';
                    div.querySelector('#entry').style.display = 'none';
                    div.querySelector('#cancel_button').style.display = 'block';
                    div.querySelector('#cancel_button').onclick = () => {
                        div.querySelector('#edit_form').style.display = 'none';
                        div.querySelector('#entry').style.display = 'block';
                        div.querySelector('#cancel_button').style.display = 'none';
                    }
                }

                const postid = div.querySelector('#entry').dataset.id;
                div.querySelector('#edit_form').onsubmit = (event) => {
                    event.preventDefault();

                    // Call sendform and chain the next fetch request
                    sendform(postid, div)
                        .then(() => {
                            // Fetch the updated post content after successful form submission
                            return fetch(`/post/${postid}`);
                        })
                        .then(response => {
                            if (!response.ok) {
                                throw new Error('Network response was not ok');
                            }
                            return response.json();
                        })
                        .then(data => {
                            div.querySelector('#entry').innerHTML = data.content;
                            console.log(data.content);
                        })
                        .catch(error => {
                            console.error('Error:', error);
                        })
                        .finally(() => {
                            // Hide the form and show the content
                            div.querySelector('#edit_form').style.display = 'none';
                            div.querySelector('#entry').style.display = 'block';
                            div.querySelector('#cancel_button').style.display = 'none';
                        });
                }
            }

            function sendform(post_id, div) {
                return fetch(`/edit/${post_id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        id: post_id,
                        new_input: div.querySelector('#edit_box').value
                    })
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log(data);
                    });
            }

            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
        });
    });


    // Logic for liking

    document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('#like_form').forEach(form => {
        // Initial fetch to set the correct button value
        let postid = form.dataset.id;
        updateLikeButton(form, postid);

        form.onsubmit = (event) => {
            event.preventDefault();

            // Perform the like/unlike action
            fetch(`like/${postid}`)
                .then(response => response.json())
                .then(result => {
                    console.log(result);
                    // Update the button value based on the new like status
                    updateLikeButton(form, postid);
                });
        };
    });
});

function updateLikeButton(form, postid) {
    fetch(`liked/${postid}`)
        .then(response => response.json())
        .then(result => {
            if (result.message == 'false') {
                form.querySelector('input').value = "Like";
            } else {
                form.querySelector('input').value = "Unlike";
            }
            form.querySelector('#num_likes').innerHTML = result.likes;
        })
        .catch(error => {
            console.error('Error:', error);
        });

}

