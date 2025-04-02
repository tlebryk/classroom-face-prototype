const express = require('express');
const app = express();

app.use(express.json());
app.use(express.static('public'));

// In-memory data store for classroom layout
// In a real application, this would be in a database
let classroomData = {
    classroomId: 'classroom1',
    tables: [
        {
            tableId: 'table1',
            seats: [
                { seatId: 'table1-seat1', student: null },
                { seatId: 'table1-seat2', student: null },
                { seatId: 'table1-seat3', student: null },
                { seatId: 'table1-seat4', student: null },
                { seatId: 'table1-seat5', student: null },
                { seatId: 'table1-seat6', student: null }
            ]
        },
        {
            tableId: 'table2',
            seats: [
                { seatId: 'table2-seat1', student: null },
                { seatId: 'table2-seat2', student: null },
                { seatId: 'table2-seat3', student: null },
                { seatId: 'table2-seat4', student: null },
                { seatId: 'table2-seat5', student: null },
                { seatId: 'table2-seat6', student: null }
            ]
        }
    ]
};

// Update endpoint to handle seat changes
app.post('/api/classroom/update', (req, res) => {
    const { studentId, name, seatId, confidence, lastSeen } = req.body;
    console.log('Received classroom update:', req.body);

    // Extract table ID and seat position from the seatId (like "seat5")
    const seatNumber = parseInt(seatId.replace('seat', ''), 10);
    const tableIndex = Math.floor((seatNumber - 1) / 6); // Each table has 6 seats
    const seatIndex = (seatNumber - 1) % 6;

    if (isNaN(seatNumber) || tableIndex >= classroomData.tables.length || seatIndex >= 6) {
        return res.status(400).json({ status: 'error', message: 'Invalid seat ID' });
    }

    const table = classroomData.tables[tableIndex];
    const seat = table.seats[seatIndex];

    // Update the student information
    seat.student = name ? {
        studentId,
        name,
        confidence,
        lastSeen
    } : null;

    res.status(200).json({ status: 'success', data: classroomData });
});

// Get endpoint to retrieve current classroom data
app.get('/api/classroom', (req, res) => {
    res.status(200).json(classroomData);
});

// Export the app for testing
module.exports = app;

// Only start the server if this file is executed directly
if (require.main === module) {
    const PORT = process.env.PORT || 3000;
    app.listen(PORT, () => {
        console.log(`Frontend service listening on port ${PORT}`);
    });
}