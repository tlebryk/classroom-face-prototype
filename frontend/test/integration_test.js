const request = require('supertest');
const app = require('../main'); // Adjust the path if needed

describe('Frontend API Integration Tests', () => {
    it('should update classroom and return success', (done) => {
        request(app)
            .post('/api/classroom/update')
            .send({
                studentId: 'stu123',
                name: 'Alice Johnson',
                seatId: 'seat5',
                confidence: 0.92,
                lastSeen: '2025-03-28T12:34:56Z'
            })
            .expect(200)
            .expect('Content-Type', /json/)
            .expect({ status: 'success' }, done);
    });

    it('should return initial classroom layout', (done) => {
        request(app)
            .get('/api/classroom?classroomId=default')
            .expect(200)
            .expect('Content-Type', /json/)
            .expect((res) => {
                if (!res.body.seats) throw new Error('Missing seats data');
            })
            .end(done);
    });
});
