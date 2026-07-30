const { dbQuery } = require('../config/database');

class Enrollment {
    static async create(userId, courseId) {
        const result = await dbQuery.run(
            "INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)",
            [userId, courseId]
        );
        return result.lastID;
    }
}

module.exports = Enrollment;
