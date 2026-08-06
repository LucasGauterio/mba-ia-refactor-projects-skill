const express = require('express');
const settings = require('./config/settings');
const { initDb } = require('./config/database');
const routes = require('./routes');
const errorHandler = require('./middlewares/errorHandler');

const app = express();
app.use(express.json());

// Init Database and Start Server
initDb()
    .then(() => {
        // Mount all routes
        app.use('/api', routes);

        // Error Handler Middleware (must be registered after routes)
        app.use(errorHandler);

        app.listen(settings.port, () => {
            console.log(`Frankenstein LMS rodando na porta ${settings.port}...`);
        });
    })
    .catch((err) => {
        console.error("Falha ao inicializar o banco de dados:", err);
        process.exit(1);
    });

module.exports = app;
