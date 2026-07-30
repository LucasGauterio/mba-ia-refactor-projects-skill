const { dbQuery } = require('../config/database');

class AuditLog {
    static async create(action) {
        const result = await dbQuery.run(
            "INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))",
            [action]
        );
        return result.lastID;
    }
}

module.exports = AuditLog;
