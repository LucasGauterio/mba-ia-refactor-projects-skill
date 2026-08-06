const { db } = require('../config/database');

class EnrollmentModel {
    static create(userId, courseId) {
        return new Promise((resolve, reject) => {
            db.run("INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)", [userId, courseId], function(err) {
                if (err) return reject(err);
                resolve(this.lastID);
            });
        });
    }
}

module.exports = EnrollmentModel;
