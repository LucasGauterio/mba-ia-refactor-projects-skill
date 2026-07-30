const { dbQuery } = require('../config/database');

class User {
    static async findById(id) {
        return dbQuery.get("SELECT * FROM users WHERE id = ?", [id]);
    }

    static async findByEmail(email) {
        return dbQuery.get("SELECT * FROM users WHERE email = ?", [email]);
    }

    static async create(name, email, hashedPassword) {
        const result = await dbQuery.run(
            "INSERT INTO users (name, email, pass) VALUES (?, ?, ?)",
            [name, email, hashedPassword]
        );
        return result.lastID;
    }

    static async delete(id) {
        // Enforcing cascade delete is handled by database ON DELETE CASCADE,
        // but we just run the delete query.
        const result = await dbQuery.run("DELETE FROM users WHERE id = ?", [id]);
        return result.changes > 0;
    }
}

module.exports = User;
