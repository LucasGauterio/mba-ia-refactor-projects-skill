const sqlite3 = require('sqlite3').verbose();
const settings = require('./settings');
const { hashPassword } = require('./security');

const db = new sqlite3.Database(settings.databasePath);

// Enable Foreign Keys
db.run("PRAGMA foreign_keys = ON", (err) => {
    if (err) {
        console.error("Erro ao ativar Foreign Keys do SQLite:", err);
    } else {
        console.log("Foreign Keys do SQLite ativadas com sucesso.");
    }
});

function initDb() {
    return new Promise((resolve, reject) => {
        db.serialize(() => {
            // Create tables with AUTOINCREMENT and FOREIGN KEYs to ensure referential integrity
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

            // Seed if database is empty
            db.get("SELECT COUNT(*) as count FROM users", [], (err, row) => {
                if (err) {
                    return reject(err);
                }
                if (row.count === 0) {
                    console.log("Banco vazio. Executando seed de dados iniciais...");
                    const hashedPass = hashPassword('123');
                    
                    db.run("INSERT INTO users (name, email, pass) VALUES (?, ?, ?)", 
                        ['Leonan', 'leonan@fullcycle.com.br', hashedPass], 
                        function(err) {
                            if (err) return reject(err);
                            
                            db.run("INSERT INTO courses (title, price, active) VALUES (?, ?, ?), (?, ?, ?)",
                                ['Clean Architecture', 997.00, 1, 'Docker', 497.00, 1],
                                function(err) {
                                    if (err) return reject(err);
                                    
                                    db.run("INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)",
                                        [1, 1],
                                        function(err) {
                                            if (err) return reject(err);
                                            
                                            db.run("INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)",
                                                [1, 997.00, 'PAID'],
                                                function(err) {
                                                    if (err) return reject(err);
                                                    console.log("Seed de dados executado com sucesso.");
                                                    resolve();
                                                }
                                            );
                                        }
                                    );
                                }
                            );
                        }
                    );
                } else {
                    console.log("Banco já inicializado. Pulando seed.");
                    resolve();
                }
            });
        });
    });
}

module.exports = {
    db,
    initDb
};
