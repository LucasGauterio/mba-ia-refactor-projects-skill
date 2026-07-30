const fs = require('fs');
const path = require('path');

// Basic manual parsing of .env file to load into process.env if available
const envPath = path.join(__dirname, '../../.env');
if (fs.existsSync(envPath)) {
    const envConfig = fs.readFileSync(envPath, 'utf8');
    envConfig.split(/\r?\n/).forEach(line => {
        const trimmed = line.trim();
        if (trimmed && !trimmed.startsWith('#')) {
            const index = trimmed.indexOf('=');
            if (index !== -1) {
                const key = trimmed.substring(0, index).trim();
                const value = trimmed.substring(index + 1).trim();
                if (key) {
                    process.env[key] = value;
                }
            }
        }
    });
}

const config = {
    port: parseInt(process.env.PORT, 10) || 3000,
    paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || "pk_test_fallback",
    adminToken: process.env.ADMIN_TOKEN || "admin-token-fallback",
    dbUser: process.env.DB_USER || "admin_master",
    dbPass: process.env.DB_PASS || "fallback_pass",
    smtpUser: process.env.SMTP_USER || "no-reply@fallback.com",
    dbPath: process.env.DATABASE_PATH || path.join(__dirname, '../../lms.db')
};

module.exports = config;
