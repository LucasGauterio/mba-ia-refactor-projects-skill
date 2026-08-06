const { db } = require('../config/database');

class UserModel {
    static findById(id) {
        return new Promise((resolve, reject) => {
            db.get("SELECT * FROM users WHERE id = ?", [id], (err, row) => {
                if (err) return reject(err);
                resolve(row);
            });
        });
    }

    static findByEmail(email) {
        return new Promise((resolve, reject) => {
            db.get("SELECT * FROM users WHERE email = ?", [email], (err, row) => {
                if (err) return reject(err);
                resolve(row);
            });
        });
    }

    static create(name, email, hashedPassword) {
        return new Promise((resolve, reject) => {
            db.run("INSERT INTO users (name, email, pass) VALUES (?, ?, ?)", [name, email, hashedPassword], function(err) {
                if (err) return reject(err);
                resolve(this.lastID);
            });
        });
    }

    static delete(id) {
        return new Promise((resolve, reject) => {
            db.run("DELETE FROM users WHERE id = ?", [id], function(err) {
                if (err) return reject(err);
                resolve(this.changes);
            });
        });
    }
}

module.exports = UserModel;
