document.addEventListener('DOMContentLoaded', function () {
    // Store the current classroom data
    let classroomData = null;

    // Function to fetch the latest classroom data from the server
    async function fetchClassroomData() {
        try {
            const response = await fetch('/api/classroom');
            if (!response.ok) {
                throw new Error('Failed to fetch classroom data');
            }
            const data = await response.json();

            // Update the UI with the new data
            if (JSON.stringify(data) !== JSON.stringify(classroomData)) {
                classroomData = data;
                renderClassroom(data);
            }
        } catch (error) {
            console.error('Error fetching classroom data:', error);
        }
    }

    // Initial data fetch
    fetchClassroomData();

    // Set up polling to fetch updates every 3 seconds
    setInterval(fetchClassroomData, 3000);

    // Function to render the classroom
    function renderClassroom(data) {
        const classroomElement = document.getElementById('classroom');
        classroomElement.innerHTML = '';

        data.tables.forEach(table => {
            const tableContainer = document.createElement('div');
            tableContainer.className = 'table-container';

            const tableElement = document.createElement('div');
            tableElement.className = 'table';
            tableElement.id = table.tableId;

            const tableLabel = document.createElement('div');
            tableLabel.className = 'table-label';
            tableLabel.textContent = table.tableId;
            tableElement.appendChild(tableLabel);

            tableContainer.appendChild(tableElement);

            // Add seats to the table
            table.seats.forEach((seat, index) => {
                const seatElement = document.createElement('div');
                seatElement.className = `seat seat-${index + 1}`;
                seatElement.id = seat.seatId;

                const nameElement = document.createElement('div');
                nameElement.className = 'seat-name';

                if (seat.student) {
                    nameElement.textContent = seat.student.name;
                    if (seat.student.confidence) {
                        // Optional: Show confidence level with color or styling
                        const confidence = parseFloat(seat.student.confidence);
                        if (confidence > 0.8) {
                            nameElement.style.borderColor = '#4CAF50'; // Green for high confidence
                        } else if (confidence > 0.5) {
                            nameElement.style.borderColor = '#FFC107'; // Yellow for medium confidence
                        } else {
                            nameElement.style.borderColor = '#F44336'; // Red for low confidence
                        }
                    }
                } else {
                    nameElement.textContent = 'Empty';
                    nameElement.style.color = '#999';
                }

                seatElement.appendChild(nameElement);
                tableContainer.appendChild(seatElement);
            });

            classroomElement.appendChild(tableContainer);
        });
    }
});