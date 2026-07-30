const sqlite3 = require('sqlite3').verbose();
const config = require('./settings');

const db = new sqlite3.Database(config.dbPath, (err) => {
    if (err) {
        console.error('Error connecting to database:', err.message);
    } else {
        db.run('PRAGMA foreign_keys = ON;', (err) => {
            if (err) console.error('Error enabling foreign keys:', err.message);
        });
    }
});

// Helper to run queries with promises
const dbQuery = {
    get: (sql, params = []) => {
        return new Promise((resolve, reject) => {
            db.get(sql, params, (err, row) => {
                if (err) reject(err);
                else resolve(row);
            });
        });
    },
    all: (sql, params = []) => {
        return new Promise((resolve, reject) => {
            db.all(sql, params, (err, rows) => {
                if (err) reject(err);
                else resolve(rows);
            });
        });
    },
    run: function (sql, params = []) {
        return new Promise((resolve, reject) => {
            db.run(sql, params, function (err) {
                if (err) reject(err);
                else resolve({ lastID: this.lastID, changes: this.changes });
            });
        });
    },
    serialize: (callback) => {
        return new Promise((resolve, reject) => {
            db.serialize(() => {
                try {
                    callback();
                    resolve();
                } catch (err) {
                    reject(err);
                }
            });
        });
    }
};

function initDb() {
    return new Promise((resolve, reject) => {
        db.serialize(() => {
            db.run(`CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT NOT NULL, 
                email TEXT UNIQUE NOT NULL, 
                pass TEXT NOT NULL
            )`);
            db.run(`CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                title TEXT NOT NULL, 
                price REAL NOT NULL, 
                active INTEGER DEFAULT 1
            )`);
            db.run(`CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                user_id INTEGER NOT NULL, 
                course_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
            )`);
            db.run(`CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                enrollment_id INTEGER NOT NULL, 
                amount REAL NOT NULL, 
                status TEXT NOT NULL,
                FOREIGN KEY (enrollment_id) REFERENCES enrollments(id) ON DELETE CASCADE
            )`);
            db.run(`CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                action TEXT NOT NULL, 
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )`);

            // Seed initial data if users table is empty
            db.get("SELECT COUNT(*) as count FROM users", (err, row) => {
                if (err) {
                    reject(err);
                    return;
                }
                if (row && row.count === 0) {
                    const crypto = require('crypto');
                    // Hash "123" for seed user
                    const salt = crypto.randomBytes(16).toString('hex');
                    const hash = crypto.pbkdf2Sync('123', salt, 100000, 64, 'sha512').toString('hex');
                    const hashedPwd = `${salt}:${hash}`;

                    db.run("INSERT INTO users (name, email, pass) VALUES ('Leonan', 'leonan@fullcycle.com.br', ?)", [hashedPwd], function(err) {
                        if (err) return reject(err);
                        db.run("INSERT INTO courses (title, price, active) VALUES ('Clean Architecture', 997.00, 1), ('Docker', 497.00, 1)", [], function(err) {
                            if (err) return reject(err);
                            db.run("INSERT INTO enrollments (user_id, course_id) VALUES (1, 1)", [], function(err) {
                                if (err) return reject(err);
                                db.run("INSERT INTO payments (enrollment_id, amount, status) VALUES (1, 997.00, 'PAID')", [], function(err) {
                                    if (err) return reject(err);
                                    resolve();
                                });
                            });
                        });
                    });
                } else {
                    resolve();
                }
            });
        });
    });
}

module.exports = { db, dbQuery, initDb };
