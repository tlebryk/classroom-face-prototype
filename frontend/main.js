const express = require('express');
const app = express();

app.use(express.json());

app.post('/api/classroom/update', (req, res) => {
    console.log('Received classroom update:', req.body);
    res.status(200).json({ status: 'success' });
});

app.get('/api/classroom', (req, res) => {
    const classroomLayout = {
        classroomId: req.query.classroomId || 'default',
        seats: [
            {
                seatId: 'seat5',
                student: {
                    studentId: 'stu123',
                    name: 'Alice Johnson'
                },
                lastSeen: "2025-03-28T12:34:56Z"
            }
        ]
    };
    res.status(200).json(classroomLayout);
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
