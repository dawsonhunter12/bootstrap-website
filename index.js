document.addEventListener('DOMContentLoaded', async () => {
    const table = document.getElementById('partsTable');
    if (!table) {
        console.error('Table not found');
        return;
    }

    try {
        // Fetch parts from the backend
        const response = await fetch('http://localhost:5000/api/parts');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const parts = await response.json();

        const tbody = table.getElementsByTagName('tbody')[0];
        tbody.innerHTML = ''; // Clear existing rows

        parts.forEach(part => {
            const row = document.createElement('tr');
            row.classList.add('text-center');

            row.innerHTML = `
                <th scope="row">${part.partNumber}</th>
                <td>${part.partName}</th>
                <td>${part.oemNumber}</td>
                <td>${part.description}</td>
                <td>${part.manufacturer}</td>
                <td>${part.quantity}</td>
                <td>${part.minStock}</td>
                <td>${part.price}</td>
                <td>${part.location}</td>
                <td>${part.notes}</td>
                <td>
                    <button type="button" class="btn btn-primary edit-button">Edit</button>
                    <button type="button" class="btn btn-danger delete-button">Delete</button>
                </td>
            `;

            // Add event listener to the delete button
            const deleteButton = row.querySelector('.delete-button');
            deleteButton.addEventListener('click', async () => {
                await fetch(`http://localhost:5000/api/parts/${part.id}`, {
                    method: 'DELETE'
                });
                row.remove();
                console.log(`Deleted part: ${part.partNumber}`);
            });

            tbody.appendChild(row);
        });

        console.log(parts);
    } catch (error) {
        console.error('Failed to fetch parts:', error);
    }
});