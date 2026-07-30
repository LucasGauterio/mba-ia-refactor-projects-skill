const { dbQuery } = require('../config/database');

class Payment {
    static async create(enrollmentId, amount, status) {
        const result = await dbQuery.run(
            "INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)",
            [enrollmentId, amount, status]
        );
        return result.lastID;
    }
}

module.exports = Payment;
