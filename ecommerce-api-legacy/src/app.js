const express = require('express');
const { initDb } = require('./config/database');
const routes = require('./routes');
const errorHandler = require('./middlewares/errorHandler');
const settings = require('./config/settings');

const app = express();
app.use(express.json());

// Load main routes
app.use(routes);

// Centralized error handler
app.use(errorHandler);

// Initialize DB and start server
initDb()
    .then(() => {
        app.listen(settings.port, () => {
            console.log(`Frankenstein LMS rodando na porta ${settings.port}...`);
        });
    })
    .catch(err => {
        console.error('Failed to initialize database:', err);
        process.exit(1);
    });
