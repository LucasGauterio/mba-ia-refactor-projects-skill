const { db } = require('../config/database');

class CheckoutModel {
    static execute({ userId, courseId, amount, status, auditAction }) {
        return new Promise((resolve, reject) => {
            db.serialize(() => {
                db.run("BEGIN TRANSACTION", (err) => {
                    if (err) return reject(err);

                    // 1. Create Enrollment
                    db.run(
                        "INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)", 
                        [userId, courseId], 
                        function(err) {
                            if (err) {
                                return db.run("ROLLBACK", () => reject(err));
                            }
                            const enrollmentId = this.lastID;

                            // 2. Create Payment
                            db.run(
                                "INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)", 
                                [enrollmentId, amount, status], 
                                function(err) {
                                    if (err) {
                                        return db.run("ROLLBACK", () => reject(err));
                                    }

                                    // 3. Create Audit Log
                                    db.run(
                                        "INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))", 
                                        [auditAction], 
                                        function(err) {
                                            if (err) {
                                                return db.run("ROLLBACK", () => reject(err));
                                            }

                                            db.run("COMMIT", (err) => {
                                                if (err) {
                                                    return db.run("ROLLBACK", () => reject(err));
                                                }
                                                resolve({ enrollmentId });
                                            });
                                        }
                                    );
                                }
                            );
                        }
                    );
                });
            });
        });
    }
}

module.exports = CheckoutModel;
