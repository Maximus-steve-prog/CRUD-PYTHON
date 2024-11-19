$(document).ready(function() {

    loadUsers();

    function loadUsers(){
        
        $.get("/users", function(data) {
            console.log(data);
            $('#usersList').empty();
            data.forEach(function(user) {
                $('#usersList').append(`<tr>
                                            <td><img src="static/images/${user.image}" style="width: 50px; height:50px;"/></td>
                                            <td>${user.name}</td>
                                            <td>${user.email}</td>
                                            <td>${user.password}</td>
                                            <td>${user.role}</td>
                                            <td><button id='${user.id}' class='edit'>Edit</button> <button id='${user.id} ' class='delete'>Delete</button></td>
                                        </tr>`);
            });
        });
    }

    $('#userForm').on('submit', function(e) {
        e.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            url: '/users',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                console.log(response.status);
                if(response.status == 202){
                    alert(response.error)
                }
                loadUsers();
            },
            error: function(xhr) {
                alert(xhr.responseJSON.error);
            }
        });
    });


    $('body').on('click', '.edit', function() {
        const id = $(this).attr('id');
        $.ajax({
            url: `/edit/${id}`,
            type: 'GET',
            success: function(response) {
                if (response.error) {
                    // Handle the error if the user wasn't found
                    alert(response.error);
                } else {
                    // Populate your form fields with the user data
                    $('#name').val(response.name); // Example input
                    $('#email').val(response.email); // Example input
                    $('#role').val(response.IdRole);
    
                    // Show the modal or form for editing
                }
            },
            error: function(xhr, status, error) {
                alert("An error occurred while fetching user data: " + error);
            }
        });
    });


    $('body').on('click', '.delete', function() {
        id = $(this).attr('id');
        $.ajax({
            url: `/delete/${id}`,
            type: 'DELETE',
            success: function(response) {
                console.log(response)
                loadUsers();
            },
            error: function(xhr, status, error) {
                alert("An error occurred while fetching user data: " + error);
            }
        });
    });





});